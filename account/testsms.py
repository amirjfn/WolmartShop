import ghasedakpack


sms = ghasedakpack.Ghasedak('2abca38de138f1b7181033bcbf73347077490ec8872a6cdf0d2d072a2c7e115b')

sms.verification({'receptor': '','type': '1','template': 'randcode','param1': '5647'})