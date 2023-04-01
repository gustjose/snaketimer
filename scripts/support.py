from datetime import timedelta

def convert_time(minutos):
    h, m = divmod(timedelta(minutes=minutos).total_seconds(), 3600)
    m, s = divmod(m, 60)

    s_o = f"0{int(s)}"
    m_o = f"0{int(m)}"
    h_o = f"0{int(h)}"

    temp = h_o[-2:] + ":" + m_o[-2:] + ":" + s_o[-2:]

    return temp

def convert_ct(segundos):
    h, m = divmod(segundos, 3600)
    m, s = divmod(m, 60)

    s_o = f"0{int(s)}"
    m_o = f"0{int(m)}"
    h_o = f"0{int(h)}"

    temp = h_o[-2:] + ":" + m_o[-2:] + ":" + s_o[-2:]

    return temp