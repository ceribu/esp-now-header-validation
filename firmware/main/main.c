#include "esp_log.h"
#include "esp_wifi.h"
#include "esp_now.h"
#include "nvs_flash.h"

#include <string.h>

const uint8_t MAC_ADDR_BROADCAST[ESP_NOW_KEY_LEN] = {0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF};
const uint8_t CHANNEL = 1;

static const char *LOG_TAG = "invalid-headers";

void espnow_add_broadcast_peer()
{
    esp_now_peer_info_t *peer = calloc(1, sizeof(esp_now_peer_info_t));
    peer->channel = CHANNEL;
    peer->ifidx = WIFI_IF_STA;
    peer->encrypt = false;
    memcpy(peer->peer_addr, MAC_ADDR_BROADCAST, ESP_NOW_ETH_ALEN);

    ESP_ERROR_CHECK(esp_now_add_peer(peer));
    free(peer);
}

static void espnow_send_cb(const uint8_t *mac_addr, esp_now_send_status_t status)
{
    if (status != ESP_NOW_SEND_SUCCESS)
    {
        ESP_LOGE(LOG_TAG, "failed to send");
        return;
    }
}

static void espnow_recv_cb(const uint8_t *mac_addr, const uint8_t *data, int len)
{
    if (mac_addr == NULL)
    {
        ESP_LOGE(LOG_TAG, "empty mac address");
        return;
    }

    if (data == NULL)
    {
        ESP_LOGE(LOG_TAG, "no data received");
        return;
    }

    if (len < 1)
    {
        ESP_LOGE(LOG_TAG, "invalid length");
        return;
    }

    ESP_LOGI(LOG_TAG, "received %d bytes from " MACSTR " data: %s", len, MAC2STR(mac_addr), data);
    for (uint16_t i = 0; i < len; i++)
    {
        printf("0x%02X ", data[i]);
    }
    printf("\n");
}

void app_main(void)
{
    ESP_ERROR_CHECK(nvs_flash_init());
    ESP_ERROR_CHECK(esp_netif_init());
    ESP_ERROR_CHECK(esp_event_loop_create_default());

    wifi_init_config_t cfg = WIFI_INIT_CONFIG_DEFAULT();
    ESP_ERROR_CHECK(esp_wifi_init(&cfg));
    ESP_ERROR_CHECK(esp_wifi_set_mode(WIFI_MODE_STA));
    ESP_ERROR_CHECK(esp_wifi_start());
    ESP_ERROR_CHECK(esp_wifi_set_channel(CHANNEL, CHANNEL));

    uint8_t mac_addr[ESP_NOW_ETH_ALEN];
    ESP_ERROR_CHECK(esp_wifi_get_mac(WIFI_IF_STA, mac_addr));

    ESP_ERROR_CHECK(esp_now_init());
    ESP_ERROR_CHECK(esp_now_register_send_cb(espnow_send_cb));
    ESP_ERROR_CHECK(esp_now_register_recv_cb(espnow_recv_cb));

    espnow_add_broadcast_peer();

    while (true)
        vTaskDelay(5000 / portTICK_RATE_MS);
}
