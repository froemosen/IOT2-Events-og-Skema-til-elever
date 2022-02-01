from ifttt_webhook import IftttWebhook

# IFTTT Webhook key, available under "Documentation"
# at  https://ifttt.com/maker_webhooks/.
IFTTT_KEY = 'bEOACrKudUx-DNoZ2icG0J'

# Create an instance of the IftttWebhook class,
# passing the IFTTT Webhook key as parameter.
ifttt = IftttWebhook(IFTTT_KEY)

# Trigger the IFTTT event defined by event_name with the content
# defined by the value1, value2 and value3 parameters.
ifttt.trigger('fest', value1='LIGMA', value2='BA', value3='LZ')