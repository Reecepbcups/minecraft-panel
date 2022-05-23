### Akash Client
```
# Install the Client 
# https://docs.akash.network/guides/cli/streamlined-steps/install-the-akash-client

cd ~
AKASH_VERSION="$(curl -s "https://raw.githubusercontent.com/ovrclk/net/master/mainnet/version.txt")"
curl https://raw.githubusercontent.com/ovrclk/akash/master/godownloader.sh | sh -s -- "v$AKASH_VERSION"
sudo mv ./bin/akash /usr/local/bin

akash keys add hot-wallet --recover
akash tx cert generate client --from hot-wallet --overwrite
akash tx cert publish client --from hot-wallet --gas-prices="0.025uakt" --gas="auto" --gas-adjustment=1.15 --node http://135.181.181.122:28957 --chain-id akashnet-2
# new cert is at ~/.akash/<YOUR-ADDRESS>.pem
```