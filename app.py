import streamlit as st
import time
import requests
import random
import string
import re
import time

def generate_random_string(length, chars=string.ascii_letters):
    return ''.join(random.choice(chars) for _ in range(length))

def generate_random_phone():
    return ''.join(random.choice(string.digits) for _ in range(10))

def generate_random_company_name():
    return generate_random_string(random.randint(5, 10))

def get_mail():
    company = generate_random_company_name()
    return generate_random_string(15) + "@" + company + random.choice([".com", ".in", ".co", ".org", ".net"])

def generate_nessus_key(app_type="nessus"):
    """Trả về dict {'success': True, 'email': str, 'key': str} hoặc {'success': False, 'error': str}"""
    random_first_name = generate_random_string(random.randint(5, 10))
    random_last_name = generate_random_string(random.randint(4, 8))
    random_phone = generate_random_phone()
    random_company = generate_random_company_name()
    email = get_mail()

    data = {
        "skipContactLookup": "true",
        "product": app_type,
        "first_name": random_first_name,
        "last_name": random_last_name,
        "email": email,
        "partnerId": "",
        "phone": random_phone,
        "title": "Test",
        "company": random_company,
        "companySize": "10-49",
        "pid": "",
        "utm_source": "",
        "utm_campaign": "",
        "utm_medium": "",
        "utm_content": "",
        "utm_promoter": "",
        "utm_term": "",
        "alert_email": "",
        "_mkto_trk": "",
        "mkt_tok": "",
        "lookbook": "",
        "gclid": "",
        "country": "US",
        "region": "",
        "zip": "",
        "apps": [app_type],
        "tempProductInterest": "Tenable Nessus Professional",
        "gtm": {"category": "Nessus Pro Eval"},
        "queryParameters": "",
        "referrer": ""
    }

    try:
        url = 'https://www.tenable.com/evaluations/api/v2/trials'
        response = requests.post(url, json=data, timeout=30)
        
        if response.status_code == 200:
            regex = r'"code":"([A-Z0-9-]+)"'
            matches = re.search(regex, response.text)
            if matches:
                activation_code = matches.group(1)
                return {
                    'success': True, 
                    'email': email, 
                    'key': activation_code,
                    'type': app_type.capitalize()
                }
        return {'success': False, 'error': f"API failed: {response.status_code} - {response.text[:200]}"}
    except Exception as e:
        return {'success': False, 'error': str(e)}


st.code("""
╦   ╦╔═╗╦╔═╔═╗╦═╗  ╔╗╔╔═╗╔═╗╔═╗╦ ╦╔═╗
║   ║║ ║╠╩╗║╣ ╠╦╝  ║║║║╣ ╚═╗╚═╗║ ║╚═╗
╩═╝╚╝╚═╝╩ ╩╚═╝╩╚═  ╝╚╝╚═╝╚═╝╚═╝╚═╝╚═╝      
     === By LEQUANGQUOCKHANH - BOYSiTinh ===
""", language="text")
st.title("🔑 Nessus Key Generator")

# Sidebar chọn loại
app_type = st.sidebar.selectbox("Chọn loại Nessus key:", ["nessus", "expert"])

# Button generate
if st.button("🎯 Tạo Activation Key", type="primary", use_container_width=True):
    with st.spinner("Đang gọi API Tenable... Chờ 10-30s"):
        result = generate_nessus_key(app_type)
        
    if result['success']:
        st.success("✅ Tạo key thành công!")
        st.balloons()  # Hiệu ứng vui
        col1, col2 = st.columns([1, 2])
        with col1:
            st.metric("Loại", result['type'])
        with col2:
            st.code(result['key'])
        st.info(f"📧 Email đăng ký: **{result['email']}**")
    else:
        st.error(f"❌ Lỗi: {result['error']}")

# Hiển thị trạng thái trước đó (session state)
if 'last_result' in st.session_state:
    st.info("**Key cuối cùng:**")
    st.code(st.session_state.last_result['key'] if st.session_state.last_result['success'] else "Lỗi")
