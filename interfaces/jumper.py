from opcua import Client, ua

# OPC UA server address
opcua_url = "opc.tcp://192.168.100.19:2035/"

# Initialize OPC UA client
client = Client(opcua_url)

try:
    # Connect to the OPC UA server
    client.connect()
    print("Connected to OPC UA Server")

    # Get the parent node (Jumpdrive Object)
    jumpdrive_node = client.get_node("i=20001")  # NodeId for the Jumpdrive object

    # Get children of the jumpdrive_node to inspect its structure
    children = jumpdrive_node.get_children()
    print("Children of Jumpdrive Node:")
    for child in children:
        print(f"Child: {child}")

    # Fetch the method node dynamically using get_child()
    jump_to_method_node = jumpdrive_node.get_child(["0:JumpTo"])  # BrowseName for JumpTo

    # Prepare input arguments (as described in the NodeSet for JumpTo method)
    x_input = ua.Variant(100, ua.VariantType.Double)  # Replace with actual value for x
    y_input = ua.Variant(200, ua.VariantType.Double)  # Replace with actual value for y

    # Call the JumpTo method using the fetched method node
    print("Calling JumpTo method...")
    result = jumpdrive_node.call_method(jump_to_method_node, x_input, y_input)

    # Display the result of the JumpTo method call
    print(f"JumpTo Result: {result}")

finally:
    # Disconnect from the OPC UA server
    client.disconnect()
    print("Disconnected from OPC UA Server")
