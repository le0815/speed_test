import speedtest
sp = speedtest.Speedtest(secure=True)
print("Tìm kiếm server....")
sp.get_servers()
print("Chọn server tốt nhất...")
sp.get_best_server()
ping_result = sp.results.ping
print(f"Độ trễ: {ping_result}ms")
print("Lấy thông tin...")
info = sp.get_config()
country = info["client"]["country"]
print(f'Quốc gia: {country}')
isp = info["client"]["isp"]
print(f'Nhà cung cấp: {isp}')
ip_addr = info["client"]["ip"]
print(f'Địa chỉ IP: {ip_addr}')

print("Đo tốc độ tải xuống...")
# down_result = sp.download()
# down_result = round(down_result / 1024 / 1024, 2)
# print(f"Tốc độ tải xuống: {down_result}Mbps")
print("Đo tốc độ tải lên...")
up_result = sp.upload()
up_result = round(up_result / 1024 / 1024, 2)
print(f"Tốc độ tải lên: {up_result}Mbps")
print(f"upload: {sp.upload_result}")
