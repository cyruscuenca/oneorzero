import copy
import re
import time

def map_if_exists(data, key, product, selectors):
    
    node = copy.deepcopy(product)
    for selector in selectors:

        if selector in node:

            node = node[selector]
    
    node_type = type(node)
    if node_type is not list and node_type is not dict:

        data[key] = node

    if node_type is str:

        if node_type == 'No':

            node = False

        if node_type == 'Yes':

            node = True    

    return data
        
def normalize_processor(product):

    data = {}
    mapping = [
        ['launch_date', ['attributes', 'BornOnDate', 'value']],
        ['cache', ['attributes', 'Cache', 'value']],
        ['use_case', ['attributes', 'CertifiedUseConditions', 'value']],
        ['clock_speed', ['attributes', 'ClockSpeed', 'value']],
        ['boost_speed', ['attributes', 'ClockSpeedMax', 'value']],
        ['code_name', ['attributes', 'CodeNameText', 'value']],
        ['core_count', ['attributes', 'CoreCount', 'value']],
        ['documentation', ['attributes', 'DatasheetUrl', 'value']],
        ['ecc_memory_support', ['attributes', 'ECCMemory', 'rawValue']],
        ['multithreading', ['attributes', 'HyperThreading', 'rawValue']],
        ['tdp', ['attributes', 'MaxTDP', 'value']],
        ['max_memory_speed', ['attributes', 'MemoryMaxSpeedMhz', 'value']],
        ['memory_type', ['attributes', 'MemoryTypes', 'value']],
        ['max_memory_channel_support', ['attributes', 'NumMemoryChannels', 'value']],
        ['max_pci_express_lane_support', ['attributes', 'NumPCIExpressPorts', 'value']],
        ['optane_support', ['attributes', 'OptaneMemorySupport', 'rawValue']],
        ['pci_express_revision', ['attributes', 'PCIExpressRevision', 'value']],
        ['package_size', ['attributes', 'PackageSize', 'value']],
        ['socket_support', ['attributes', 'SocketsSupported', 'value']],
        ['status', ['attributes', 'StatusCodeText', 'value']],
        ['intel_turbo_boost_version', ['attributes', 'TBTVersion', 'value']],
        ['release_date', ['onMarketDateTime']],
        ['bit_width', ['attributes', 'EM64', 'rawValue']],
        ['features', ['attributes', 'Filter-IntelTechnology', 'rawValue']],
        ['lithography', ['attributes', 'Filter-Lithography', 'value']],
        ['sku', ['attributes', 'RetailSkuAvailable', 'rawValue']],
    ]

    for item in mapping:
        
        data = map_if_exists(data, item[0], product, item[1])

    data['name'] = None
    if 'rawName' in product:

        data['name'] =  re.sub(r'\(.*\)', '', product['rawName'])
    
    # Not sure about this. This should fill lots of null values, but 16 and 8 bit width
    # processors are a thing
    data['bit_width'] = '32-bit'
    if 'EM64' in product['attributes'] and 'rawValue' in product['attributes']['EM64'] and bool(product['attributes']['EM64']['rawValue']):

        data['bit_width'] = '64-bit'

    # Pipe seperated list of IDs (string)
    if 'features' in data:

        data['features'] = data['features'].split('|')

    if 'lithography' in product['attributes']:

        data['lithography'] = data['lithography'].replace(' ', '')

    if 'TCase' in product['attributes']:

        data['max_temp_on_ihs'] = product['attributes']['TCase']['value']

    if 'mediaAssets' in product:

        data['image'] = product['mediaAssets']
        for image in data['image']:

            if image['identifier'] == 'standard_image':

                data['image'] = image
                break
            
            if image['identifier'] == 'product_image_1':

                data['image'] = image
                break

            if image['identifier'] == 'picture_1':

                data['image'] = image
                break

    return True