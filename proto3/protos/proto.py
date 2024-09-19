import grpc
import api_pb2
import api_pb2_grpc


def run():
    # Connect to the gRPC server
    with grpc.insecure_channel('192.168.100.19:2028') as channel:
        stub = api_pb2_grpc.HackingDeviceServerStub(channel)

        # Create an empty Void message
        request = api_pb2.Void()

        # Call the read_secret_station_data method
        response = stub.read_secret_station_data(request)

        # Print the received data
        print("Received data:")
        for item in response.data:
            print(item)


if __name__ == '__main__':
    run()
