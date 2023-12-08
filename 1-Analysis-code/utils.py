import os
import shutil


def is_clean_domain(domain_name):
    if domain_name.find('tsinghua') != -1:
        return True
    elif domain_name.find('windows') != -1:
        return True
    elif domain_name.find('microsoft') != -1:
        return True
    elif domain_name.find("azure") != -1:
        return True
    elif domain_name.find('mozilla') != -1:
        return True
    elif domain_name.find("firefox") != -1:
        return True

    clean_lst = {
        "ns-1627.awsdns-11.co.uk",
        "ns-cloud-b1.googledomains.com",
        "e12437.d.akamaiedge.net",
        "kv801.prod.do.dsp.mp.microsoft.com",
        "displaycatalog.mp.microsoft.com",
        "download.windowsupdate.com",
        "ns1.phicdn.net",
        "a1952.dscq.akamai.net",
        "msedge.api.cdp.microsoft.com",
        "glb.api.prod.dcat.dsp.trafficmanager.net",
        "l-0007.l-msedge.net",
        "e16646.ca.s.tl88.net",
        "k256.gslb.ksyuncdn.com",
        "glb.sls.prod.dcat.dsp.trafficmanager.net",
        "msedge.f.dl.delivery.mp.microsoft.com",
        "tsfe.trafficshaping.dsp.mp.microsoft.com",
        "ocsp.digicert.com",
        "fe2cr.update.microsoft.com",
        "g-msn-com-nsatc.trafficmanager.net",
        "fe-platformcn-maps-atm.trafficmanager.net",
        "storeedgefd.dsx.mp.microsoft.com",
        "prod.ingestion-edge.prod.dataops.mozgcp.net",
        "incoming.telemetry.mozilla.org",
        "tsfe.trafficmanager.net",
        "geo-prod.do.dsp.mp.microsoft.com",
        "www.bing.com",
        "fe3cr.delivery.mp.microsoft.com",
        "fp2e7a.wpc.phicdn.net",
        "ns-cloud-d1.googledomains.com",
        "r3.o.lencr.org",
        "dev.ditu.live.com",
        "firefox.settings.services.mozilla.com",
        "prod.content-signature-chains.prod.webservices.mozgcp.net",
        "china.bing123.com",
        "config.edge.skype.com",
        "content-signature-2.cdn.mozilla.net",
        "public1.114dns.com",
        "prod.balrog.prod.cloudops.mozgcp.net",
        "g.live.com",
        "glb.cws.prod.dcat.dsp.trafficmanager.net",
        "apps.identrust.com",
        "slscr.update.microsoft.com",
        "cacerts.digicert.com",
        "msedge.b.tlu.dl.delivery.mp.microsoft.com",
        "settings-win.data.microsoft.com",
        "a1887.dscq.akamai.net",
        "aus5.mozilla.org"
    }

    return domain_name in clean_lst


def get_malicious_domain_names():
    with open('./statistical_result/malicious_domains.txt', 'r') as f:
        lst = f.read().split('\n')
    return lst


if __name__ == '__main__':
    d = '/path/to/dir'
    for sample_id in os.listdir(d):
        print(sample_id)
        if os.path.exists(f'{d}/{sample_id}/reports/report.json'):
            # shutil.copyfile(f'{d}\\{sample_id}\\reports\\report.json', f'./reports/{sample_id}.json')
            shutil.copyfile(f'{d}/{sample_id}/dump.pcap', f'/path/to/newdir/{sample_id}.pcap')
            
