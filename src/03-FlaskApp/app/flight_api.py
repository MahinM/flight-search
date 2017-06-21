import redis
import datetime
from dateutil import parser

conn = redis.Redis(host='xxxxxxxxxxxxxxx', password='xxxxxxxxxxxxx', port=6379, encoding='utf-8')
seconds_in_day = 24 * 60 * 60
seconds_in_hour = 60 * 60

def unix_time_millis(dt):
    epoch = datetime.datetime.utcfromtimestamp(0)
    return (dt - epoch).total_seconds() 

def get_flights(origin,destination,travel_date):
   results =  {}
   direct_flight_list = []
   if conn.exists('flights:' + origin.upper() + ':' + destination.upper()):
      start_time = unix_time_millis(parser.parse(travel_date))
      end_time = start_time + seconds_in_day

      conn.zinterstore('flights_by_route',['flights:' + origin + ":" + destination,'departure:'],aggregate='max')

      distance = str(conn.get('distance:' + origin + ':' + destination),'utf-8')

      #Assemble structure to return
      for f in conn.zrangebyscore('flights_by_route', start_time, end_time, withscores=True):
         result = conn.hgetall(f[0])
         if int(result[b'availability']) > 0:
            item =  {}
            item['origin'] = origin
            item['destination'] = destination
            item['distance'] = distance
            item['time'] = datetime.datetime.fromtimestamp(f[1])
            item['flight'] = str(f[0],'utf-8').split(':')[1]
            item['availability'] = str(result[b'availability'],'utf-8')
            item['price'] =  str(result[b'price'],'utf-8')
            item['carrier'] = str(result[b'carrier'],'utf-8')
            direct_flight_list.append(item)
      results['direct_flights'] = direct_flight_list


      connecting_flight_list = []
      connections = conn.sinter('routes:' + origin, 'routes:' + destination)

      if len(connections) > 0:
         for hop in connections:
            hop = str(hop,'utf-8')
            leg1 = origin + ':' + hop
            leg2 = hop + ':' + destination

            #intersect route and departure to find flights for that route
            conn.zinterstore('flights_by_route_hop1',['flights:' + leg1,'departure:'],aggregate='max')
            #intersect route and departure to find flights for part 2
            conn.zinterstore('flights_by_route_hop2',['flights:' + leg2,'departure:'],aggregate='max')

            distance_leg1 = str(conn.get('distance:' + leg1),'utf-8')
            distance_leg2 = str(conn.get('distance:' + leg2),'utf-8')

            #filter the flights on the route to the given day
            for f in conn.zrangebyscore('flights_by_route_hop1',start_time, 
               end_time, withscores=True):
               flight1_str = {}
               flight1 = conn.hgetall(f[0])
               flight1_str['departure'] = datetime.datetime.fromtimestamp(f[1])
               flight1_str['origin'] = origin
               flight1_str['destination'] = hop
               flight1_str['distance'] = distance_leg1
               flight1_str['flight'] = str(f[0],'utf-8').split(':')[1]
               flight1_str['availability'] = str(flight1[b'availability'],'utf-8')
               flight1_str['price'] =  str(flight1[b'price'],'utf-8')
               flight1_str['carrier'] = str(flight1[b'carrier'],'utf-8') 


               conn.zinterstore('flights_by_carrier', ['flights_by_route_hop2', 'carrier:' + flight1_str['carrier']], aggregate='max')
               for f2 in conn.zrangebyscore('flights_by_carrier', f[1] + seconds_in_hour, 
                  end_time, withscores=True):
                  flight2 = conn.hgetall(f2[0])
                  flight2_str = {}
                  flight2_str['departure'] = datetime.datetime.fromtimestamp(f2[1])
                  flight2_str['origin'] = hop
                  flight2_str['destination'] = destination
                  flight2_str['distance'] = distance_leg2
                  flight2_str['flight'] = str(f2[0],'utf-8').split(':')[1]
                  flight2_str['flight'] = str(f[0],'utf-8').split(':')[1]
                  flight2_str['availability'] = str(flight1[b'availability'],'utf-8')

                  connecting_flight_list.append([flight1_str,flight2_str])

   results["connecting_flights"] = connecting_flight_list
   return results
