
akash commands (instances since closed)
akash q deployment list --log_format json --node http://135.181.181.122:28957
akash q deployment get --dseq 5751573 --owner akash1rpv97xasy7px29ccdhy93ar6aj0t8a6895d4n3 --node http://135.181.181.122:28957

akash provider lease-logs --dseq 5751573 --follow --tail 10 --provider akash1r7y2msa9drwjss5umza854he5vwr2czunye9de --from hot-wallet --node http://135.181.181.122:28957
akash provider lease-shell --dseq 5751573 --provider akash1r7y2msa9drwjss5umza854he5vwr2czunye9de --node http://135.181.181.122:28957 --from hot-wallet --tty --stdin -- web /bin/sh

akash provider lease-shell --dseq 5751573 --provider akash1r7y2msa9drwjss5umza854he5vwr2czunye9de --node http://135.181.181.122:28957  --from hot-wallet --tty -- web ls > testls.txt

akash provider lease-shell --dseq 5751573 --provider akash1r7y2msa9drwjss5umza854he5vwr2czunye9de --node http://135.181.181.122:28957  --from hot-wallet --tty -- web rcon-cli
"akash provider lease-shell --dseq {dseq} --provider {provider} --from {WALLET_NAME} --node {RPC_NODE} --tty -- web mc-send-to-console {{COMMAND}}"
