import os
import requests
import certifi

class JenkinsClient:
    def __init__(self):
       # self.username = <load username>
       # self.token = <load token>:

        #if isinstance(self.username, str):
         #   self.username = self.username.strip()
          #  self.username=os.getenv("JENKINS_USER").strip()
        #if isinstance(self.token, str):
         #   self.token = self.token.strip()
          #  self.token=os.getenv("JENKINS_TOKEN").strip()
        
       
        # SSL Vaidation

        self.verify_ssl = os.getenv(
            "JENKINS_VERIFY_SSL",
            "false"
        ).lower() == "true"

        self.ca_bundle = os.getenv(
            "JENKINS_CA_BUNDLE",
            certifi.where()
        )


    def get_config_xml(self, url):
        print("DEBUG SSL VALUE:", self.verify_ssl)
        print("DEBUG USER:", self.username)
        print("DEBUG TOKEN LENGTH:", len(self.token) if self.token else 0)

        response=requests.get(
            url,
        print("DEBUG AUTH USER:", repr(self.username)),
        print("DEBUG AUTH TOKEN LENGTH:", len(self.token)),
            auth=(self.username, self.token),
            # print("DEBUG USER", self.username),
           # print("DEBUG TOKEN LENGTH:", len(self.token) if self.token else 0),
            verify=self.verify_ssl
       )

        response.raise_for_status()
        return response.text
