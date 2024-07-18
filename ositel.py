import requests

data={
     "data": {
        "claveSitio": "6LdcxV8dAAAAAMQZV05VmMp5TYlQJGoGQjv6FgX8",
        "claveSecreta": "null",
        "action": "consulta",
        "siteVerify": "null",
    }
}

#r=requests.post("https://checatuslineas.osiptel.gob.pe/", data=data)


#print(r.text)

data ={
"columns[0][data]": 0,
"columns[0][name]": "indice",
"order[0][column]": 0,
"order[0][dir]": "asc",
"length":200,#indica el numero de lineas que se van a mostrar
"models[IdTipoDoc]": "02",#tipo 02 es para ruc y el 01 es para dni
"models[NumeroDocumento]": 20522317285,
"models[ReCaptcha]": "03AFcWeA5-eC99avwU7qHmRhAEu5V767MTDS62HWujJf0jGJc1d0CPAGV__NToYmOG_pdtCtLrpj0_5BPnLB-Bhw5BAHSk6IE2lVRNs1Zt7iwAZJYAf2bo5Q7z_5gRJO1UpTzROA1j9SWfiWNcvubJ4gaYuL3BtA8tJGTOUbU2rHdVov-6jOmgDhTtWpKhTduALUAawPKXe9I69eHGJdyRrWv-kun2IHCuO1NiIvkqxMGL_O2_L_oQM96PxIRPhnfNTD_cTkS7ZZBh8p14TCBGSgF7E4AsCn9h8EqoF4-JJ8qyaAxKuGqMHR1DaPlhaPegyNtlmMIACjb4N00lg4X5lLiByEa9bIwyV87JpIFZ6f6L6S3zW9q6sm2Gx8l1sbAjyeftyN5FiD8qK41fdeAkwpTylAK4TgqYMv3JX8TiLCcYLJWrgRft0bRExliFKtSbHtu_Uu2VzKZmbTiAjTsqZeQ4__Z0qhkezOfGKTozNu7PfywF1di49ErQF1P5BUDJIXpVHGJhlHu_Nkfsd-q1BnaF22h9SIs7XYjtq4Hm8nSwkHNIe3wVvCME6jGFwUSBhR1-BOyEJsQ3mC8wuxJgFpgYQZ6wo6h7jyp8fDKIaN1MqrnqY_lz4QkSSXBK6NDopQqqwSedlhCScO3Fn5zCZ68KQe4zBtD0fZT0kt0m58GbxY8jWv6d_XlvLyxgfXLM29Ls6acyZ05NYXX4mRu73AVkVjuBlNK3GTMr0cvA6AXxFbQLZmHvW0TLLa42OjoWXfWzzzXCZ1cnHQB-megySjESq2LbpK33AsevtSA_ENFRtr-eRF4DMfVLq_zzEhaG8ocLxGxuYTsXnGEOGkj6mTSZLvvZJkfeEY7aszNY_hl-5ogAziO3nm_xiIVwm_Nw50EbiaeQtA5J",
"models[GoogleCaptchaTokenOLD]": "03AFcWeA6Bj5whnWtHGu2VQpz6nV3IzSkQInZSI1-b1rfL_on8CXWyhdJAThe2zkT3BydMHzbuZ8xAYv9Hns0KkItUuN8PuVDfq118u7wyOxGzqdPMQwcK6MULTGcyn8riOIJ0On-veyEHAIfAWH3vylsbApdRbsMyyBksAtERibE422Mr7JS2RHGJI_YuK6U55GDFymrs9LSmzVT_KE18CpnrXGsIhWa5N1PHOnqFq27ihJPZZl_empV7AtLoHrB_OjzA8MO3i0OD-n0xF7c1Kjo4LV5sMIhRuDj-TrJFImtCkhVAMPhxEPYAt9Oxf-Ld75W4mKWtkRZLOuYHfp3WmrH2mw8DrqZLgg2NX1jAwTXaSm4Vb84mDtOKqFfXI5o3GTo2FhqtxFUyIMbi16R_IpXZpVAYNKaGL2oXidbJalov0Cxg-c5OoGg0AfJiYkGiAHsPOd7QoFQkDLRZqfnyUG5fwFegsAH55PruFl3xhfyKKgVnEsuaHu_FYpJGGxvigQ8guZ6K47ma4wgCPSTRs2WjVPLzsMSXS1atiee3AlBFkOOzQwwbvU5qIKpx2u3BIe0aVYNE1WV5DPS5HTET6HIHDWJeQGopNJc89QoEa4AVwp_3QMKrhycjBJU-D2woYrqy1_aM7QiNNUNuQHXa-O7L3KEQYIyCCUGh716PBXJm-WUwWobIcPw7KttUG67O7mdPV956fngE5QiC4QG_AX6N0I0penNvfOLUxfpCPVxZ5cwaBZRVq8exCyimzeFShuHEO1x0ctkkx5re8TKeZn5LS0JhMFDzwCCifT_2GqFaAh8GX_0ejv8vfoAGsS2vuuXeSzUHj33mFK-_uP8FujYdgl3RLpnFDAKtAlQw6fqmExEA0B75HZw",
}
r=requests.post("https://checatuslineas.osiptel.gob.pe/Consultas/GetAllCabeceraConsulta/", data=data)

print(r.status_code)
print(r.text)