import ipaddress
import streamlit as st

def print_binary(ip):
    return '.'.join([format(int(octet), '08b') for octet in str(ip).split('.')])

st.set_page_config(page_title="Subnetting Calculator", page_icon="🌐")
st.title("🌐 Subnetting Calculator")
st.markdown("A user-friendly subnet calculator that supports **IPv4 & IPv6** 🧮")

ip_input = st.text_input("Enter IP with CIDR (e.g. 192.168.1.0/24 or 2001:db8::/64)", "192.168.1.0/24")
divide_subnet = st.checkbox("🔀 Divide into subnets?")
new_prefix = None

if divide_subnet:
    new_prefix = st.number_input("Enter new subnet prefix (e.g. 26 for IPv4 or 68 for IPv6)", min_value=1, max_value=128, step=1)

if st.button("🚀 Calculate"):
    try:
        network = ipaddress.ip_network(ip_input, strict=False)

        st.subheader("📋 Subnet Details")
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Network Address:**")
            st.code(str(network.network_address))
            st.markdown("**Broadcast Address:**")
            st.code(str(getattr(network, 'broadcast_address', 'N/A')))
            st.markdown("**Subnet Mask:**")
            st.code(str(network.netmask))
            st.markdown("**Wildcard Mask:**")
            st.code(str(network.hostmask))

        with col2:
            st.markdown("**Binary Network:**")
            st.code(print_binary(network.network_address))
            st.markdown("**Binary Mask:**")
            st.code(print_binary(network.netmask))

        if network.version == 4:
            num_hosts = network.num_addresses - 2 if network.num_addresses > 2 else 0
        else:
            num_hosts = network.num_addresses  # IPv6 usually doesn't subtract

        st.success(f"Number of Hosts: {num_hosts}")

        hosts = list(network.hosts())
        if network.version == 4 and len(hosts) >= 2:
            st.info(f"Usable Host Range: {hosts[0]} → {hosts[-1]}")
        elif len(hosts) == 1:
            st.info(f"Only Usable Host: {hosts[0]}")

        # Subnetting
        if divide_subnet and new_prefix:
            if new_prefix <= network.prefixlen:
                st.warning("New prefix must be greater than the current prefix.")
            else:
                st.subheader(f"🔹 Subnets (/ {new_prefix})")
                subnets = list(network.subnets(new_prefix=new_prefix))
                for i, subnet in enumerate(subnets[:8]):  # Display first 8 for brevity
                    st.markdown(f"`Subnet {i+1}` ➤ **{subnet}** | Hosts: {subnet.num_addresses - 2 if network.version == 4 else subnet.num_addresses}")
                if len(subnets) > 8:
                    st.markdown(f"...and {len(subnets) - 8} more.")
    except ValueError as e:
        st.error(f"❌ Error: {e}")
