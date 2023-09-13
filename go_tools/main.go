package main

import (
	"context"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"os"

	"github.com/crowdstrike/gofalcon/falcon"
	"golang.org/x/oauth2/clientcredentials"
)

type Config struct {
	FALCON_CLIENT_ID     string `json:"FALCON_CLIENT_ID"`
	FALCON_CLIENT_SECRET string `json:"FALCON_CLIENT_SECRET"`
	FALCON_CLOUD         string `json:"FALCON_CLOUD"`
}

// getFalconToken retrieves an OAuth2 token for accessing the Falcon API
func getFalconToken(clientId string, clientSecret string, clientCloud string) string {
	config := clientcredentials.Config{
		ClientID:     clientId,
		ClientSecret: clientSecret,
		TokenURL:     "https://" + falcon.Cloud(clientCloud).Host() + "/oauth2/token",
	}
	token, err := config.Token(context.Background())
	if err != nil {
		panic(err)
	}
	return token.AccessToken
}

func readConfig(filename string) (*Config, error) {
	data, err := ioutil.ReadFile(filename)
	if err != nil {
		return nil, err
	}
	var config Config
	if err := json.Unmarshal(data, &config); err != nil {
		return nil, err
	}
	return &config, nil
}

func main() {
	// Read the configuration from a secure file
	config, err := readConfig("config.json")
	if err != nil {
		fmt.Println("Error reading config file:", err)
		os.Exit(1)
	}

	// Get Falcon API OAuth2 token
	accessToken := getFalconToken(config.FALCON_CLIENT_ID, config.FALCON_CLIENT_SECRET, config.FALCON_CLOUD)

	// Output the access token (for debugging purposes; do not expose this in a production environment)
	fmt.Println(accessToken)
}
