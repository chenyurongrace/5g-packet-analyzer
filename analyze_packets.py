from scapy.all import rdpcap
from collections import Counter, defaultdict
from scapy.layers.inet import TCP
from scapy.packet import Raw
import matplotlib.pyplot as plt
import datetime

try:
    packets = rdpcap("data/5g_packets.pcap")
    print(f"✅ Successfully loaded {len(packets)} packets.\n")

    for i, pkt in enumerate(packets[:5]):
        print(f"Packet {i+1}: {pkt.summary()}")

except Exception as e:
    print("❌ Failed to read pcap file:", e)
    exit(1)


# Count protocol layers
layer_counter = Counter()
for pkt in packets:
    for layer in pkt.layers():
        layer_counter[layer.__name__] += 1

print("\n📊 Protocol Layer Distribution:")
for layer, count in layer_counter.most_common():
    print(f"{layer:<15}: {count} packets")

# Pie chart of protocol layers
if layer_counter:
    labels = list(layer_counter.keys())
    sizes = list(layer_counter.values())

    plt.figure(figsize=(6, 6))
    plt.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=140)
    plt.title("Protocol Layer Distribution")
    plt.axis("equal")
    plt.tight_layout()
    plt.savefig("assets/protocol_pie.png")
    plt.show()


print("\n📦 HTTP Requests/Responses (from Raw payloads):")
http_count = 0

for pkt in packets:
    if pkt.haslayer(TCP) and pkt.haslayer(Raw):
        try:
            payload = pkt[Raw].load.decode("utf-8", errors="ignore")
            if payload.startswith(("GET", "POST", "HTTP")):
                http_count += 1
                print(f"\n--- HTTP Packet #{http_count} ---\n{payload.strip()}")
        except Exception:
            pass

if http_count == 0:
    print("⚠️ No HTTP traffic detected in payloads.")


# Count packets per second
time_bins = defaultdict(int)
for pkt in packets:
    timestamp = int(pkt.time)
    time_bins[timestamp] += 1

sorted_times = sorted(time_bins.keys())
counts = [time_bins[t] for t in sorted_times]
readable_times = [datetime.datetime.fromtimestamp(t).strftime('%H:%M:%S') for t in sorted_times]

# Plot line chart
plt.figure(figsize=(8, 4))
plt.plot(readable_times, counts, marker='o')
plt.title("Packet Count Over Time")
plt.xlabel("Time (HH:MM:SS)")
plt.ylabel("Packet Count")
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("assets/packet_trend.png")
plt.show()






# from scapy.all import rdpcap
# from collections import Counter

# try:
#     packets = rdpcap("data/5g_packets.pcap")
#     print(f"✅ 成功读取 {len(packets)} 个数据包")

#     for i, pkt in enumerate(packets[:5]):
#         print(f"Packet {i+1}: {pkt.summary()}")

#     # 👉 统计协议层
#     layer_counter = Counter()
#     for pkt in packets:
#         for layer in pkt.layers():
#             layer_counter[layer.__name__] += 1

#     print("\n📊 协议层统计：")
#     for layer, count in layer_counter.most_common():
#         print(f"{layer:<15}: {count} 个包")

# except Exception as e:
#     print("❌ 读取失败：", e)


# import matplotlib.pyplot as plt

# # 🟢 绘制协议层分布饼图
# if layer_counter:
#     labels = list(layer_counter.keys())
#     sizes = list(layer_counter.values())

#     plt.figure(figsize=(6, 6))
#     plt.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=140)
#     plt.title("Protocol Layer Distribution")
#     plt.axis("equal")
#     plt.tight_layout()
#     plt.show()


# from scapy.layers.inet import TCP
# from scapy.packet import Raw

# print("\n🧾 HTTP 请求/响应内容（来自 Raw 载荷）：")

# http_count = 0

# for pkt in packets:
#     # 只处理有 Raw 数据的 TCP 包
#     if pkt.haslayer(TCP) and pkt.haslayer(Raw):
#         try:
#             payload = pkt[Raw].load.decode("utf-8", errors="ignore")
#             if payload.startswith("GET") or payload.startswith("POST") or payload.startswith("HTTP"):
#                 http_count += 1
#                 print(f"\n📦 HTTP 包 #{http_count} 内容预览:\n{payload.strip()}")
#         except Exception as e:
#             pass

# if http_count == 0:
#     print("⚠️ 没有检测到 HTTP 请求或响应内容")

    
# from collections import defaultdict
# import matplotlib.pyplot as plt
# import datetime

# # 🕒 统计每秒的包数量
# time_bins = defaultdict(int)

# for pkt in packets:
#     timestamp = int(pkt.time)  # 精确到秒
#     time_bins[timestamp] += 1

# # 排序时间轴
# sorted_times = sorted(time_bins.keys())
# counts = [time_bins[t] for t in sorted_times]
# readable_times = [datetime.datetime.fromtimestamp(t).strftime('%H:%M:%S') for t in sorted_times]

# # 📈 画出折线图
# plt.figure(figsize=(8, 4))
# plt.plot(readable_times, counts, marker='o')
# plt.title("Packet Count Over Time")
# plt.xlabel("Time (HH:MM:SS)")
# plt.ylabel("Packet Count")
# plt.grid(True)
# plt.xticks(rotation=45)
# plt.tight_layout()
# plt.show()
# plt.savefig("packet_trend.png")


