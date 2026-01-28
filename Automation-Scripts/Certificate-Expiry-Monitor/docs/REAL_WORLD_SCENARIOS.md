# 🌍 Real-World Scenarios - Certificate Expiry Monitor

Praktyczne przykłady użycia systemu w rzeczywistych środowiskach produkcyjnych.

---

## 👨‍💼 Scenariusz 1: Administrator Sieci Korporacyjnej

### Profil
- **Firma:** Średnia korporacja (500 pracowników)
- **Infrastruktura:** 50+ certyfikatów SSL/TLS
- **Środowisko:** 
  - Strona WWW (public-facing)
  - Portal pracowniczy (intranet)
  - Mail server (SMTP/IMAP)
  - VPN gateway
  - Load balancers (F5, HAProxy)
  - API endpoints

### Problem
W 2025 roku certyfikat na głównej stronie WWW wygasł w weekend. Firma straciła 50,000 PLN przychodu przez 12 godzin przestoju.

### Rozwiązanie z Certificate Expiry Monitor

#### Krok 1: Inwentaryzacja Certyfikatów

Admin tworzy listę wszystkich certyfikatów w `config/domains.yml`:

    domains:
      # Public-facing services
      - host: www.firma.pl
        port: 443
        name: "Strona główna (Public)"
        enabled: true
        
      - host: api.firma.pl
        port: 443
        name: "REST API (Public)"
        enabled: true
        
      - host: portal.firma.pl
        port: 443
        name: "Portal pracowniczy (Intranet)"
        enabled: true
        
      # Mail servers
      - host: mail.firma.pl
        port: 993
        protocol: imaps
        name: "Mail Server (IMAPS)"
        enabled: true
        
      - host: mail.firma.pl
        port: 465
        protocol: smtps
        name: "Mail Server (SMTPS)"
        enabled: true
        
      # VPN & Network
      - host: vpn.firma.pl
        port: 443
        name: "VPN Gateway (SSL)"
        enabled: true
        
      - host: 192.168.1.100
        port: 443
        name: "Load Balancer (F5)"
        enabled: true
        
      # External services (vendors)
      - host: erp.dostawca.pl
        port: 443
        name: "System ERP (Dostawca)"
        enabled: true

#### Krok 2: Konfiguracja Alertów

W `.env` ustawia:

    # Wyślij WARNING 60 dni przed wygaśnięciem (2 miesiące na odnowienie)
    ALERT_WARNING_DAYS=60

    # Wyślij CRITICAL 14 dni przed (pilny alarm)
    ALERT_CRITICAL_DAYS=14

    # Email do zespołu IT
    EMAIL_TO=admin@firma.pl,devops@firma.pl,boss@firma.pl

    # Slack dla DevOps
    SLACK_WEBHOOK_URL=https://hooks.slack.com/services/XXX
    SLACK_ENABLED=True

#### Krok 3: Automatyzacja (Linux Cron)

Admin dodaje do crona (uruchom codziennie o 8:00):

    0 8 * * * cd /opt/cert-monitor && /usr/bin/python3 scripts/main.py --check-now >> /var/log/cert-monitor.log 2>&1

#### Krok 4: Dashboard dla Szefa

Co tydzień admin generuje raport HTML i wysyła do managementu:

    python scripts/main.py --check-now --no-alerts --formats html
    
    # Wyślij email z załącznikiem
    echo "Tygodniowy raport certyfikatów SSL/TLS" | mail -s "SSL Report" -A output/reports/certificate_report_*.html boss@firma.pl

#### Rezultat

- ✅ **60 dni przed wygaśnięciem:** Admin dostaje email "WARNING - www.firma.pl"
- ✅ **Odnawia certyfikat** spokojnie w ciągu 2 tygodni (np. przez Let's Encrypt)
- ✅ **Brak przestojów** - certyfikat odnowiony 30 dni przed wygaśnięciem
- ✅ **Szef zadowolony** - widzi proaktywne działanie IT

---

## 🚀 Scenariusz 2: DevOps Engineer w Startupie

### Profil
- **Firma:** Startup technologiczny (20 osób)
- **Infrastruktura:** 
  - Kubernetes cluster (AWS EKS)
  - 15 microservices z Ingress Controller
  - CI/CD pipeline (Jenkins, GitLab)
  - Monitoring (Prometheus, Grafana)

### Problem
Mikroservisy używają różnych certyfikatów (Ingress TLS secrets). Ciężko śledzić ręcznie które wygasają.

### Rozwiązanie

#### Integracja z CI/CD Pipeline

DevOps dodaje skrypt do GitLab CI/CD (`.gitlab-ci.yml`):

    cert-check:
      stage: monitor
      script:
        - python3 scripts/main.py --check-now --threshold 30
        - |
          if grep -q "CRITICAL" output/reports/certificate_report_*.csv; then
            echo "❌ Critical certificates found!"
            exit 1
          fi
      only:
        - schedules  # Uruchom tylko przez scheduler (daily)
      artifacts:
        paths:
          - output/reports/
        expire_in: 7 days

#### Webhook do Slack

Konfiguruje `.env`:

    SLACK_WEBHOOK_URL=https://hooks.slack.com/services/XXX
    SLACK_ENABLED=True
    
    # Wyślij alert do kanału #devops
    SLACK_CHANNEL=#devops

#### Automatyczne Odnowienie (cert-manager w K8s)

Gdy dostanie alert, DevOps sprawdza cert-manager:

    kubectl get certificates -A
    kubectl describe certificate api-tls -n production

Jeśli cert-manager nie odnowił automatycznie, ręcznie triggeruje:

    kubectl delete secret api-tls -n production
    # cert-manager automatycznie wygeneruje nowy

#### Rezultat

- ✅ **Proaktywne alerty** w Slack
- ✅ **Zero manual work** - cert-manager + monitoring
- ✅ **CI/CD sprawdza** certyfikaty przed deploymentem
- ✅ **Grafana dashboard** (opcjonalnie - import JSON reports)

---

## 🏢 Scenariusz 3: MSP (Managed Service Provider)

### Profil
- **Firma:** Dostawca usług IT dla 50 klientów
- **Infrastruktura:** 
  - 200+ certyfikatów (różni klienci)
  - Mix: Apache, Nginx, IIS, Load Balancers
  - Różne providery: Let's Encrypt, DigiCert, Sectigo

### Problem
Każdy klient ma swoje certyfikaty. Ręczne sprawdzanie = 8h/tydzień. Zdarzały się wygaśnięcia (niezadowoleni klienci).

### Rozwiązanie

#### Multi-Tenant Configuration

MSP tworzy osobne pliki `domains-*.yml` dla każdego klienta:

    config/
    ├── domains-klient1.yml
    ├── domains-klient2.yml
    ├── domains-klient3.yml
    └── ...

**Przykład `domains-klient1.yml`:**

    domains:
      - host: klient1.pl
        port: 443
        name: "Klient 1 - Strona główna"
        enabled: true
        
      - host: shop.klient1.pl
        port: 443
        name: "Klient 1 - Sklep"
        enabled: true

#### Skrypt Wrapper (Bash)

    #!/bin/bash
    # check-all-clients.sh
    
    for client in config/domains-*.yml; do
        echo "Checking $client..."
        python3 scripts/main.py --config "$client" --check-now
    done
    
    # Połącz wszystkie raporty
    python3 scripts/merge_reports.py output/reports/*.json > output/master_report.json

#### Dashboard dla Klientów

MSP udostępnia każdemu klientowi **personalny raport HTML** (co tydzień email):

    # Generuj raport tylko dla Klienta 1
    python3 scripts/main.py --config config/domains-klient1.yml --formats html
    
    # Wyślij email
    mail -s "SSL Report - Klient 1" -A output/reports/klient1_*.html kontakt@klient1.pl

#### Billing Integration

MSP liczy certyfikaty jako część SLA:

    # Eksportuj do CSV dla fakturowania
    python3 scripts/main.py --check-now --formats csv
    
    # Import do systemu billing
    python3 scripts/billing_import.py output/reports/certificate_report_*.csv

#### Rezultat

- ✅ **Automatyzacja 200+ certyfikatów** - 8h → 30 minut/tydzień
- ✅ **Proaktywne alerty** dla każdego klienta
- ✅ **Profesjonalne raporty** - klient widzi że MSP dba o szczegóły
- ✅ **Unikanie kar SLA** - zero przestojów przez wygasłe certyfikaty

---

## 🔒 Scenariusz 4: Security Team (Audyt Bezpieczeństwa)

### Profil
- **Firma:** Bank (wymogi regulacyjne)
- **Cel:** Audyt certyfikatów SSL/TLS zgodnie z PCI-DSS

### Wymagania PCI-DSS

- ✅ Wszystkie certyfikaty muszą być ważne
- ✅ Minimalna długość klucza: RSA 2048-bit
- ✅ Zakaz słabych algorytmów: MD5, SHA-1
- ✅ TLS 1.2+ (zakaz TLS 1.0, TLS 1.1)
- ✅ Comiesięczny raport dla audytora

### Rozwiązanie

#### Konfiguracja `settings.yml`:

    validation:
      check_key_strength: true
      min_key_size: 2048
      
      forbidden_algorithms:
        - MD5
        - SHA1
      
      min_tls_version: "1.2"

#### Scheduled Audit (Pierwszy dzień miesiąca)

    # Cron: 1-go każdego miesiąca o 8:00
    0 8 1 * * cd /opt/cert-monitor && python3 scripts/main.py --check-now --audit-mode >> /var/log/audit.log 2>&1

#### Raport dla Audytora

    # Generuj JSON + CSV (dla audytora)
    python3 scripts/main.py --check-now --formats json,csv
    
    # Podpisz cyfrowo (dla non-repudiation)
    gpg --sign output/reports/certificate_report_*.json

#### Compliance Dashboard

Security team importuje JSON do Splunk/ELK:

    # Wyślij do SIEM
    curl -X POST https://splunk.firma.pl:8088/services/collector \
         -H "Authorization: Splunk XXX" \
         -d @output/reports/certificate_report_*.json

#### Rezultat

- ✅ **Compliance PCI-DSS** - automatyczny audyt
- ✅ **Dokumentacja dla regulatora** - raporty JSON podpisane cyfrowo
- ✅ **Zero weak ciphers** - skrypt wykrywa i alarmuje
- ✅ **Audyt passed** - bank spełnia wymogi

---

## 🌐 Scenariusz 5: SaaS Platform (Multi-Region)

### Profil
- **Firma:** SaaS provider (globalna platforma)
- **Infrastruktura:** 
  - 5 regionów AWS (us-east-1, eu-west-1, ap-southeast-1, ...)
  - CloudFront CDN (własne certyfikaty)
  - Route53 (DNS failover)

### Problem
Certyfikaty w każdym regionie wygasają niezależnie. CloudFront wymaga odnowienia przed wygaśnięciem (brak automatycznego renewal).

### Rozwiązanie

#### Multi-Region Monitoring

    domains:
      # US East (Virginia)
      - host: us-api.saas.com
        port: 443
        name: "API US-EAST-1"
        enabled: true
        
      # EU West (Ireland)
      - host: eu-api.saas.com
        port: 443
        name: "API EU-WEST-1"
        enabled: true
        
      # Asia Pacific (Singapore)
      - host: ap-api.saas.com
        port: 443
        name: "API AP-SOUTHEAST-1"
        enabled: true
        
      # CloudFront
      - host: d123456.cloudfront.net
        port: 443
        name: "CDN CloudFront"
        enabled: true

#### AWS Lambda Integration (Serverless)

DevOps wdraża skrypt jako **AWS Lambda** (uruchamiana przez CloudWatch Events):

    # Lambda handler
    def lambda_handler(event, context):
        import subprocess
        result = subprocess.run(['python3', 'scripts/main.py', '--check-now'], capture_output=True)
        
        # Wyślij raport do SNS topic
        sns.publish(TopicArn='arn:aws:sns:us-east-1:123:cert-alerts', Message=result.stdout)

#### Terraform/IaC

Infrastruktura jako kod (automatyczne deployment):

    resource "aws_cloudwatch_event_rule" "cert_check" {
      name                = "cert-expiry-check"
      schedule_expression = "cron(0 8 * * ? *)"  # Codziennie o 8:00 UTC
    }

    resource "aws_cloudwatch_event_target" "lambda" {
      rule      = aws_cloudwatch_event_rule.cert_check.name
      target_id = "cert-monitor-lambda"
      arn       = aws_lambda_function.cert_monitor.arn
    }

#### Rezultat

- ✅ **Global monitoring** - wszystkie regiony w jednym miejscu
- ✅ **Serverless** - zero infrastructure overhead
- ✅ **SNS → PagerDuty** - alerty 24/7
- ✅ **IaC** - pełna automatyzacja

---

## 📊 Porównanie Scenariuszy

| Scenariusz | Liczba Certów | Alerty | Automatyzacja | ROI (czas zaoszczędzony) |
|------------|---------------|--------|---------------|--------------------------|
| Korporacja | 50+ | Email, Slack | Cron (Linux) | 4h/tydzień → 30 min |
| Startup DevOps | 15 | Slack | GitLab CI/CD | 2h/tydzień → 15 min |
| MSP (50 klientów) | 200+ | Email per client | Bash wrapper | 8h/tydzień → 30 min |
| Bank (Security) | 30 | SIEM (Splunk) | Monthly audit | Compliance achieved |
| SaaS (Global) | 20 (multi-region) | SNS → PagerDuty | AWS Lambda | 24/7 monitoring |

---

## 🎯 Best Practices (Wszystkie Scenariusze)

### 1. Progi Alertów

- **WARNING:** 60 dni (dla manualnych procesów odnowienia)
- **CRITICAL:** 14 dni (dla automatycznych procesów)
- **EXPIRED:** 0 dni (natychmiastowa eskalacja)

### 2. Redundancja Alertów

Nie polegaj tylko na jednym kanale:

    # .env
    EMAIL_ENABLED=True
    SLACK_ENABLED=True
    TEAMS_ENABLED=True

### 3. Testuj Regularnie

Raz na kwartał wygeneruj testowy certyfikat wygasający za 1 dzień i sprawdź czy alerty działają.

### 4. Dokumentuj Procesy

Każdy alert powinien zawierać link do runbook:

    Alert: Certificate expiring in 7 days
    
    Action Required:
    1. Review renewal procedure: https://wiki.firma.pl/ssl-renewal
    2. Contact: devops@firma.pl
    3. Escalate to: boss@firma.pl (if not resolved in 24h)

### 5. Backup Certyfikatów

Zawsze trzymaj backup starych certyfikatów (dla rollback):

    /opt/certs/backup/
    ├── www.firma.pl-2025-01-01.pem
    ├── www.firma.pl-2025-06-15.pem
    └── ...

---

## 📚 Dodatkowe Zasoby

- **[Installation Guide](INSTALLATION_AND_USAGE.md)** - Jak zainstalować
- **[Docker Testing](DOCKER_TESTING.md)** - Środowisko testowe
- **[Troubleshooting](TROUBLESHOOTING.md)** - Rozwiązywanie problemów

---

**Gotowe!** Praktyczne scenariusze użycia w prawdziwym świecie! 🌍
