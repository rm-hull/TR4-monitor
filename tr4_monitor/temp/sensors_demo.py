import sensors

sensors.init()
try:
    for chip in sensors.iter_detected_chips():
        print(f'{chip} at {chip.adapter_name}')
        for feature in chip:
            print(f'  {feature.label}: {feature.get_value()}')
finally:
    sensors.cleanup()
