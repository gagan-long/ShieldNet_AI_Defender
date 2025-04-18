from pymisp import ExpandedPyMISP

def get_misp_indicators():
    misp = ExpandedPyMISP(
        url=configs.misp_url,
        key=configs.misp_key
    )
    
    events = misp.search(
        eventinfo="AI Security",
        tags=["ransomware", "llm_exploit"]
    )
    
    return [event['Event']['info'] for event in events]
