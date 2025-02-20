if sudo cp /home/pi/raspberry/mioscript.service /etc/systemd/system/mioscript.service; then
    echo "Copia di mioscript.service riuscita."
else
    echo "Errore nella copia di mioscript.service!" >&2
    exit 1
fi

if sudo cp /home/pi/raspberry/mioscript1.service /etc/systemd/system/mioscript1.service; then
    echo "Copia di mioscript1.service riuscita."
else
    echo "Errore nella copia di mioscript1.service!" >&2
    exit 1
fi

# Ricarica systemd
if sudo systemctl daemon-reload; then
    echo "Reload di systemd riuscito."
else
    echo "Errore nel reload di systemd!" >&2
    exit 1
fi

# Abilita e avvia i servizi
for service in mioscript.service mioscript1.service; do
    if sudo systemctl enable "$service"; then
        echo "Servizio $service abilitato correttamente."
    else
        echo "Errore nell'abilitazione di $service!" >&2
        exit 1
    fi

    if sudo systemctl start "$service"; then
        echo "Servizio $service avviato correttamente."
    else
        echo "Errore nell'avvio di $service!" >&2
        exit 1
    fi
done

echo "Tutti i servizi sono stati configurati e avviati con successo!"
exit 0
