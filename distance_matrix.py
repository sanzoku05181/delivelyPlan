import googlemaps
import pandas as pd
import time

API_KEY = 'AIzaSyDsJ7le3-B4HGY3o-3d-KtpvO8DTdKxhIc'
gmaps = googlemaps.Client(key=API_KEY)

locations_df = pd.read_csv('locations_spl.csv')
addresses = locations_df['address'].tolist()

distance_matrix = pd.DataFrame(index=addresses, columns=addresses)

def get_distance_matrix(origins, destinations):
    try:
        matrix = gmaps.distance_matrix(origins, destinations, mode='driving', language='ja')
        time.sleep(1)
        return matrix
    except Exception as e:
        print(f"Error: {e}")
        return None

batch_size = 10
total = len(addresses)
total_batches = (total + batch_size - 1) // batch_size

print(f"🚗 距離行列の計算を開始します（全{total_batches ** 2}バッチ）")

for i in range(0, total, batch_size):
    for j in range(0, total, batch_size):
        origin_batch = addresses[i:i+batch_size]
        dest_batch = addresses[j:j+batch_size]

        print(f"▶️ バッチ処理中: origins {i}-{i+len(origin_batch)-1}, destinations {j}-{j+len(dest_batch)-1}")
        result = get_distance_matrix(origin_batch, dest_batch)

        if result:
            for oi, origin in enumerate(origin_batch):
                for di, destination in enumerate(dest_batch):
                    try:
                        element = result['rows'][oi]['elements'][di]
                        if element['status'] == 'OK':
                            distance_km = element['distance']['value'] / 1000
                            distance_matrix.at[origin, destination] = distance_km
                        else:
                            distance_matrix.at[origin, destination] = None
                    except:
                        distance_matrix.at[origin, destination] = None

print("💾 CSVファイルに保存中...")
distance_matrix.to_csv('distance_matrix_km.csv')
print("✅ 完了: distance_matrix_km.csv を保存しました")
