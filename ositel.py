import requests
import pandas as pd
import os
import json

def main():
    
    data ={
    "columns[0][data]": 0,
    "columns[0][name]": "indice",
    "order[0][column]": 0,
    "order[0][dir]": "asc",
    "length":1000000000,#indica el numero de lineas que se van a mostrar, el maximo es 1000000000
    "models[IdTipoDoc]": 2,#tipo 02 es para ruc y el 01 es para dni
    "models[NumeroDocumento]": 20522317285,
    # "models[ReCaptcha]": "03AFcWeA5-eC99avwU7qHmRhAEu5V767MTDS62HWujJf0jGJc1d0CPAGV__NToYmOG_pdtCtLrpj0_5BPnLB-Bhw5BAHSk6IE2lVRNs1Zt7iwAZJYAf2bo5Q7z_5gRJO1UpTzROA1j9SWfiWNcvubJ4gaYuL3BtA8tJGTOUbU2rHdVov-6jOmgDhTtWpKhTduALUAawPKXe9I69eHGJdyRrWv-kun2IHCuO1NiIvkqxMGL_O2_L_oQM96PxIRPhnfNTD_cTkS7ZZBh8p14TCBGSgF7E4AsCn9h8EqoF4-JJ8qyaAxKuGqMHR1DaPlhaPegyNtlmMIACjb4N00lg4X5lLiByEa9bIwyV87JpIFZ6f6L6S3zW9q6sm2Gx8l1sbAjyeftyN5FiD8qK41fdeAkwpTylAK4TgqYMv3JX8TiLCcYLJWrgRft0bRExliFKtSbHtu_Uu2VzKZmbTiAjTsqZeQ4__Z0qhkezOfGKTozNu7PfywF1di49ErQF1P5BUDJIXpVHGJhlHu_Nkfsd-q1BnaF22h9SIs7XYjtq4Hm8nSwkHNIe3wVvCME6jGFwUSBhR1-BOyEJsQ3mC8wuxJgFpgYQZ6wo6h7jyp8fDKIaN1MqrnqY_lz4QkSSXBK6NDopQqqwSedlhCScO3Fn5zCZ68KQe4zBtD0fZT0kt0m58GbxY8jWv6d_XlvLyxgfXLM29Ls6acyZ05NYXX4mRu73AVkVjuBlNK3GTMr0cvA6AXxFbQLZmHvW0TLLa42OjoWXfWzzzXCZ1cnHQB-megySjESq2LbpK33AsevtSA_ENFRtr-eRF4DMfVLq_zzEhaG8ocLxGxuYTsXnGEOGkj6mTSZLvvZJkfeEY7aszNY_hl-5ogAziO3nm_xiIVwm_Nw50EbiaeQtA5J",
    # "models[GoogleCaptchaTokenOLD]": "03AFcWeA6Bj5whnWtHGu2VQpz6nV3IzSkQInZSI1-b1rfL_on8CXWyhdJAThe2zkT3BydMHzbuZ8xAYv9Hns0KkItUuN8PuVDfq118u7wyOxGzqdPMQwcK6MULTGcyn8riOIJ0On-veyEHAIfAWH3vylsbApdRbsMyyBksAtERibE422Mr7JS2RHGJI_YuK6U55GDFymrs9LSmzVT_KE18CpnrXGsIhWa5N1PHOnqFq27ihJPZZl_empV7AtLoHrB_OjzA8MO3i0OD-n0xF7c1Kjo4LV5sMIhRuDj-TrJFImtCkhVAMPhxEPYAt9Oxf-Ld75W4mKWtkRZLOuYHfp3WmrH2mw8DrqZLgg2NX1jAwTXaSm4Vb84mDtOKqFfXI5o3GTo2FhqtxFUyIMbi16R_IpXZpVAYNKaGL2oXidbJalov0Cxg-c5OoGg0AfJiYkGiAHsPOd7QoFQkDLRZqfnyUG5fwFegsAH55PruFl3xhfyKKgVnEsuaHu_FYpJGGxvigQ8guZ6K47ma4wgCPSTRs2WjVPLzsMSXS1atiee3AlBFkOOzQwwbvU5qIKpx2u3BIe0aVYNE1WV5DPS5HTET6HIHDWJeQGopNJc89QoEa4AVwp_3QMKrhycjBJU-D2woYrqy1_aM7QiNNUNuQHXa-O7L3KEQYIyCCUGh716PBXJm-WUwWobIcPw7KttUG67O7mdPV956fngE5QiC4QG_AX6N0I0penNvfOLUxfpCPVxZ5cwaBZRVq8exCyimzeFShuHEO1x0ctkkx5re8TKeZn5LS0JhMFDzwCCifT_2GqFaAh8GX_0ejv8vfoAGsS2vuuXeSzUHj33mFK-_uP8FujYdgl3RLpnFDAKtAlQw6fqmExEA0B75HZw",
    "models[ReCaptcha]": "03AFcWeA5CdiRf-AVC7vEHe9RgjPO6jH2u_lo24-yL7E7LaIOPJV-GHUG9tbvUwg07A0u-HriUqCiTRseWhk7TsPHzZz2CQRenAnPRuXyrMVdyNJ8SJaJtoGYKq6BPap4pmtFfUvjIj0UMF12w4y0JtAponcYxKOxBtvZuhCzTFASlRmEfdoK3NfWYq24PCnPN36eq-3Q4rUDlx9eR-Q-L5Bmy0z8vHD4_07RBG35f0EvktO0zdf83lCaRGLE_0F5NEQdoO1AdCqqtAzenDwqzvvO1kJ11ZL0H-KJFVH6NaSnwzSwb2iZKBMnTrqwLQ0O9sLgyCdY989JDNOH3cxAvm-HTJI1X97Kqis-FEFYvPB27YQlZhUxFFzZbrmnhwF9r-Bkm4s1S9DFGpYAqGggQ7Z4qv92fzRaCsrmcEv8jVaK2pfbCJqecCh-xwbSRTwQFcy_4rvKpEg6qKsAb_VfJeAQIVnJGjpHmd4HhsqWZEWLvci5V-bj-Ya5LWvq46dhVcV3kdDGhmb2Kj4lqFx3wV6gTZHxjgnAiIQgzZdRMxIkgcHvU9j8arIIrIRzRFYxXxw4pXoTsh26Lp2S40YCGjnkrlbEE1hDg23yt9zqhOc2y0f4Yx34pSbpkMspdEXQUgkmauCtXff6k8deAtx0aH3BYCTilhYHV9y_QUGZnzCyZkBZAVzfxnl6tCdEwe2AzkqQfWxhnwpqQLwHldYKM01mQMyZ-MbzXCjRWZ9fzSDxuY47j0R_L30Osh3A-mHhyPxGZpgteqxVmhifqLGzRy1zAIW1bPbSHfflXuMHXOJGqBCr5fWN65C7Iqg5YuOgUjD30DT8zgTEI8lEY56FMA4FKzQc2R1Kqseu-8Gvo-nqtGzt_vGb3YvAxrHTTlPMjo-5viXJtPpSx",
    "models[ReCaptcha]": "03AFcWeA5XcAuGWLh-ySqaQEId8A3t3rTkSJB4y_wiTAsAc-6YWxLUEZlgmZVyxFRK8UddKXy4tn515KDX4K0VJEmtvEWWX25cPPviwFOKgppF2ARPKOZpyvxpQVVCV0rBggHnVF1zDTLpJ_fvb2COT8G33dr8UOALj2xUQTHJDyeQyUfgYK1NZ2ogpL27nMZ3hOEJzU5zGezZdd-2jMn43aQ8YyMHzaLNdXU8tfwZSVZyyJpcrcG5BLT2YtlvsfQBI6vLdD3xpR9zsn1hwkHAYIppAy6BWltOoYGsYPE27uBDUriNwsHSVOokKL8LBrLr5aA7QwKpFXt1hodr_s5Gzxru5O1fThC1anGDIfZJr_aag1F3vTApKCruhZgHpMGSqQbuv5m8F7zxNK4DuhnzdfbPo0JA25XKZk7uV3LQKY_2cwedLfqZ4YYANC84hGY2m3Tp-znr-DXXebDCmUhDoCuQWFuuEYROY6iHg9ich3BAfcttdBu68SeUyzapn9nUpciCzYabj2lGtjtH7mDYp7R3S-LyEBxg9FnBxIvuSSn-nckKpXro33KoGGvFxkY5X7Dps5u7m9xHYugJZYqAl-2q4Qi6TIAKa8p2swOix4v7YUiketdw6gXC8yJZ1dogtADncr-ouzfI98md0V52afWoRYfXHNJnNnIhQVAuuW6kPEZ6cn3i91G8YSvFNc7_Hx_WYCplBE19ZdLxwLg0EBwzBnVaJE21vEUnyBbl8s92UUCqK6-f18DSzU1etxZOxE_brMq6n2uAGaE6ysbV0v6tXqM5zjLOKzBZUjl2ZYhTnsq1M-zl9CCxyDuwPaonRTtGhDaJkA9DVtf3WHiukNSSj1utYWxbzrWEu9ulol8rkIZUZUas70Jum0KqjviFL9qPtKyYhwUj",
    "models[GoogleCaptchaTokenOLD]": "03AFcWeA78qef4aTkxswwKnUlBhdDJeKpcDsfjKMBcbqrUOlTKeTu8ODmHlD9GPrdgeOau0_nGUn_HC0MywvLWJ2whKAM_FBOHghO-bCmo8kdagoCuqqcWQvCrEo-Gf83wIx9XFltndPwZmgg1-nT6r9PaZGCraPzwrGXVS6DOBF9TO96XOGqL_Kyj6I2zlxxnKojUCjFZfP9ZnDIQQm1xGXdiLN_4FdWvKJ1WeTnsPp0MPcskD22blpx8VIARX2ZE4mImo_aA0rblr0SyRyP9RSW2ZPH9XeXX0_Km5laFy-5-j0knnGYFny8jbOOHHhMw2Vnm8MG2WnrVO3YolscoyTbrgETxXiFVpewlrqGCJ4pyXVbJQ_OybXIjfIk24HjQxYWcKZS6Y5NJBC49LLwG6c_H0qz3CAHPvvip3KUKyn3joMTWt0yn8KHuIDazKMCiEfjz0kcVPjh_3VKp7KN2V15S60bTfuRVRRYRY5yW1g9JnL3xaPxe4nSgimbAjjLRWwGxBwcV6WwMsEJChTDzHtki9gq6DyWqmYqGosAIgfu6pXbjC0xI4oLVupV48NLp1XVer6DUi4Ht39keAZpxwVmFP4JPxNhTpQ1s3X-wH8oeVnUhdTG6anMgCV5OahdD-vgJuFqlI4ol9IQcBmwa_DMLo8MD7VmrYepD-XBhuP7t_fhNdorZQYgYYy-TVB3fQ5KheOKcYMDnGZKrVFnSkc1SblY5ec0z4xVQLNDhe-Z7x9MO3vcmuShd73dwaaBVEWb2ZMov1Ey0l_O1BP8aXdEiAIz0o1fq7G9DO_nfvtTkoQ-AYzP0grVvEjar_g4G6dHTwE6tAwl-8W35t3DkOB0t4i0EmIuBsW8vLRy__Gu6hPepokqFD2kDSeWOv_ZzgngM1Q6XXOfq",
    "models[GoogleCaptchaTokenOLD]": "03AFcWeA4rA5s7JKnBY9G0OBcvZ0uhnoHe1db1wXA786R_ptiDXw48uKATlSK__Ws_zmBMWnRh5v4G47nGLjRMBRruzXp1PomPh_5ySOgk0pQj4sxUReMILFd7C4L9PGkCw5cyqV-ifHAfiQFRn6yZ8y0GQ58sUvuWO3HXzXNKasIXxnlXtEsk8SmhYiyCSmDiH076nTFIfvY8WYT1OGKipDSv2uh5jJH3NYotQxFtGlP4rzaenzcNCW4shxhMSZ4ih4Mj-r6izsxZ-Ma8kYU2utIH7rhIxopWJ8hYcUpCyBsyIene8BPUXeQRzbBF14U58JspZnaOgMwOxcA5cfGKmv6SXNTwJ7_aigA7hbRy6cqx_-bA9wmIRc_PjRWWMLG7Lyar99UDU2bFr6QreK0-hZ4sEl4rpRvlAEKCuv0c59AmnWjy08HS-WMI97qRl8n30MbytlvJwXG2ISNhZpos3O--pO-NgyMGTKsokN6LtRPBaVUlXvkPCJTi5yjiWk2I-1CJdI-g0vdglKgvW28CcVPx1JVAwJJDOlLd2KofrWzsMzJAW1l3SQqAlFqLIEJFvN5nfrxWJj96nUb0AXW9R36ABNR9vIkRorRUZEkHZja4LKqbFMowis1TBfpCoH97VIhziQHysa6pQq0tQrwZY-agodX_1d1fuwTvm1-uzpXs0lUW1cQKYfilAjRvUY_yqm4PdRbwPSEbmkqeaug92u-VwS95sJyum70u7L1J72rz-gd9Ur05A4BphIAfELB3j3otcrpgXfoU7Wpe9VLUGVfOCs2jpkUCKiAt9nF_Q3cg7oYn1uq4_1vByIM7MafiSB84_5o1sAxBOQzhhWnXgTHGJAoE9MHRqjYkRNPcMtHfUvOz-5Q4xom6gey2A-_6jlUERb6B3fxR"
    }
    r=requests.post("https://checatuslineas.osiptel.gob.pe/Consultas/GetAllCabeceraConsulta/", data=data)
    print(r.status_code)
    M=0
    C=0
    E=0
    O=0
    if r.status_code ==200:
        
        response=r.json()
        print(response["iTotalRecords"])
        print(response["iTotalDisplayRecords"])
      
        for fila in response["aaData"]:
            operador=fila[3]
            if operador=="TELEFONICA DEL PERU S.A.A.":
                M+=1
            elif operador =="AMERICA MOVIL PERU S.A.C.":
                C+=1
            elif operador =="ENTEL PERU S.A.":
                E+=1
            else:
                O+=1
        print(f"LAS LINEAS MOVILES POR OPERADOR SON: M{M}C{C}E{E}O{O}")
     
    else:
        print("Ocurrio un error")
        print(r.status_code) 
if __name__=='__main__':
    main()
