# ⏰ Windows Task Scheduler - Szczegółowy Przewodnik

Automatyczne uruchamianie Infrastructure Documentation Generator na Windowsie za pomocą wbudowanego Task Scheduler (Harmonogram zadań).

---

## 📋 Spis Treści

- [Wprowadzenie](#wprowadzenie)
- [Przygotowanie](#przygotowanie)
- [Metoda 1: Konfiguracja Podstawowa](#metoda-1-konfiguracja-podstawowa)
- [Metoda 2: Konfiguracja Zaawansowana](#metoda-2-konfiguracja-zaawansowana)
- [Metoda 3: Przez PowerShell](#metoda-3-przez-powershell)
- [Testowanie Zadania](#testowanie-zadania)
- [Rozwiązywanie Problemów](#rozwiązywanie-problemów)
- [Best Practices](#best-practices)

---

## 🎯 Wprowadzenie

**Task Scheduler** to wbudowane narzędzie Windows do automatycznego uruchamiania programów w określonym czasie. Jest równoważnikiem Cron z Linuxa.

### Dlaczego Task Scheduler?

✅ Wbudowany w Windows (nie trzeba instalować)  
✅ Uruchamia zadania nawet gdy użytkownik nie jest zalogowany  
✅ Obsługa wielu triggerów (czas, event, logowanie)  
✅ Logowanie historii uruchomień  
✅ Retry przy błędzie

### Czego Potrzebujesz?

- Windows 10/11 lub Windows Server
- Uprawnienia Administrator (do tworzenia zadania)
- Skrypt już skonfigurowany i przetestowany ręcznie

---

## 🛠️ Przygotowanie

### Krok 1: Utwórz Plik Batch

Zamiast uruchamiać bezpośrednio Python, utworzymy plik `.bat` który:
- Aktywuje virtual environment
- Uruchamia skrypt
- Loguje output

**Utwórz plik:** `run_generator.bat` w głównym folderze projektu

    @echo off
    REM ======================================================================
    REM Infrastructure Documentation Generator - Batch Runner
    REM ======================================================================
    
    REM Ustaw ścieżkę do projektu
    cd /d C:\Users\YourUsername\my-it-profile-hub\Automation-Scripts\Infrastructure-Docs-Generator
    
    REM Aktywuj virtual environment
    call venv\Scripts\activate.bat
    
    REM Uruchom skrypt
    echo [%date% %time%] Uruchamiam Infrastructure Documentation Generator... >> output\logs\scheduler.log
    python scripts\main.py >> output\logs\scheduler.log 2>&1
    
    REM Zapisz exit code
    set EXIT_CODE=%ERRORLEVEL%
    echo [%date% %time%] Zakończono z kodem: %EXIT_CODE% >> output\logs\scheduler.log
    
    REM Deaktywuj venv
    call venv\Scripts\deactivate.bat
    
    exit /b %EXIT_CODE%

**Ważne:** Zmień `C:\Users\YourUsername\...` na swoją rzeczywistą ścieżkę!

### Krok 2: Przetestuj Plik Batch

Przed dodaniem do Task Scheduler, przetestuj ręcznie:

    C:\Users\YourUsername\my-it-profile-hub\Automation-Scripts\Infrastructure-Docs-Generator\run_generator.bat

Jeśli działa poprawnie, przejdź do kolejnego kroku.

---

## 🎬 Metoda 1: Konfiguracja Podstawowa (GUI)

Najprostsza metoda przez graficzny interfejs.

### Krok 1: Otwórz Task Scheduler

Naciśnij **Win + R**, wpisz:

    taskschd.msc

Naciśnij **Enter**. Otworzy się okno Task Scheduler.

### Krok 2: Create Basic Task

1. W prawym panelu kliknij: **Create Basic Task...**
2. Wypełnij formularz:

**General Tab:**

    Name: Infrastructure Documentation Generator
    Description: Automatyczne generowanie dokumentacji sieci codziennie o 2:00

Kliknij **Next**

### Krok 3: Trigger (Kiedy uruchamiać)

Wybierz: **Daily**

Kliknij **Next**

**Start Date:** Dzisiejsza data  
**Start Time:** `02:00:00` (2:00 AM)  
**Recur every:** `1` days

Kliknij **Next**

### Krok 4: Action (Co uruchamiać)

Wybierz: **Start a program**

Kliknij **Next**

**Program/script:** Pełna ścieżka do pliku batch:

    C:\Users\YourUsername\my-it-profile-hub\Automation-Scripts\Infrastructure-Docs-Generator\run_generator.bat

**Start in (optional):** Folder projektu:

    C:\Users\YourUsername\my-it-profile-hub\Automation-Scripts\Infrastructure-Docs-Generator

Kliknij **Next**

### Krok 5: Finish

Zaznacz: **Open the Properties dialog for this task when I click Finish**

Kliknij **Finish**

### Krok 6: Dodatkowe Ustawienia (Properties)

Otworzy się okno Properties. Skonfiguruj:

**General Tab:**

- Zaznacz: **Run whether user is logged on or not**
- Zaznacz: **Run with highest privileges**
- Configure for: **Windows 10** (lub Twoja wersja)

**Triggers Tab:**

Sprawdź czy trigger jest poprawny (Daily at 2:00 AM)

**Settings Tab:**

- Zaznacz: **Allow task to be run on demand**
- Zaznacz: **Run task as soon as possible after a scheduled start is missed**
- Zaznacz: **If the task fails, restart every:** `15 minutes`, Attempt to restart up to: `3 times`
- Odznacz: **Stop the task if it runs longer than:** (usuń limit czasu)

Kliknij **OK**

System poprosi o podanie hasła administratora (jeśli wybrano "Run whether user is logged on or not").

---

## 🔧 Metoda 2: Konfiguracja Zaawansowana (GUI)

Dla zaawansowanych użytkowników, którzy chcą więcej kontroli.

### Krok 1: Create Task (Advanced)

W Task Scheduler, w prawym panelu kliknij: **Create Task...** (nie Basic Task!)

### Krok 2: General Tab

    Name: Infrastructure Documentation Generator
    Description: Automatyczna dokumentacja infrastruktury sieciowej z użyciem AI

**Security options:**

- **User account:** Twoje konto administratora
- Zaznacz: **Run whether user is logged on or not**
- Zaznacz: **Run with highest privileges**
- Zaznacz: **Hidden** (zadanie nie pojawi się w Task Manager dla użytkownika)

**Configure for:** Windows 10

### Krok 3: Triggers Tab

Kliknij **New...**

**Begin the task:** `On a schedule`

**Settings:**

- Wybierz: **Daily**
- **Start:** Dzisiejsza data + `02:00:00`
- **Recur every:** `1` days

**Advanced settings:**

- Zaznacz: **Enabled**
- Odznacz: **Expire** (zadanie nie wygasa)

Kliknij **OK**

**Dodatkowy Trigger (opcjonalnie):** Uruchom również przy starcie systemu

Kliknij **New...** ponownie

    Begin the task: At startup
    Delay task for: 5 minutes (żeby system się w pełni załadował)

Kliknij **OK**

### Krok 4: Actions Tab

Kliknij **New...**

**Action:** `Start a program`

**Settings:**

    Program/script: C:\Users\YourUsername\my-it-profile-hub\Automation-Scripts\Infrastructure-Docs-Generator\run_generator.bat
    
    Start in: C:\Users\YourUsername\my-it-profile-hub\Automation-Scripts\Infrastructure-Docs-Generator

Kliknij **OK**

### Krok 5: Conditions Tab

**Idle:**

- Odznacz wszystko (nie czekaj na bezczynność)

**Power:**

- Odznacz: **Start the task only if the computer is on AC power**
- Zaznacz: **Wake the computer to run this task** (jeśli komputer w sleep mode)

**Network:**

- Zaznacz: **Start only if the following network connection is available**
- Wybierz: **Any connection** (skrypt wymaga sieci do urządzeń)

### Krok 6: Settings Tab

**If the task is already running:**

- Wybierz: **Do not start a new instance**

**If the task fails:**

- Zaznacz: **Restart every:** `15 minutes`, Attempt to restart: `3 times`

**Other:**

- Zaznacz: **Allow task to be run on demand**
- Zaznacz: **Run task as soon as possible after a scheduled start is missed**
- Odznacz: **Stop the task if it runs longer than** (bez limitu)
- Zaznacz: **If the running task does not end when requested, force it to stop**

Kliknij **OK**

System poprosi o hasło administratora.

---

## 💻 Metoda 3: Przez PowerShell (Skryptowa)

Dla tych, którzy preferują automatyzację przez kod.

### Skrypt PowerShell

Utwórz plik: `create_scheduled_task.ps1`

    # Infrastructure Documentation Generator - Task Scheduler Setup
    # Uruchom jako Administrator!
    
    # Konfiguracja
    $TaskName = "Infrastructure Documentation Generator"
    $TaskDescription = "Automatyczna dokumentacja sieci z AI"
    $ScriptPath = "C:\Users\YourUsername\my-it-profile-hub\Automation-Scripts\Infrastructure-Docs-Generator\run_generator.bat"
    $WorkingDir = "C:\Users\YourUsername\my-it-profile-hub\Automation-Scripts\Infrastructure-Docs-Generator"
    $TriggerTime = "02:00"
    
    # Sprawdź czy zadanie już istnieje
    $ExistingTask = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
    if ($ExistingTask) {
        Write-Host "Zadanie '$TaskName' już istnieje. Usuwam..." -ForegroundColor Yellow
        Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
    }
    
    # Utwórz akcję (co uruchomić)
    $Action = New-ScheduledTaskAction -Execute $ScriptPath -WorkingDirectory $WorkingDir
    
    # Utwórz trigger (kiedy uruchomić)
    $Trigger = New-ScheduledTaskTrigger -Daily -At $TriggerTime
    
    # Utwórz ustawienia
    $Settings = New-ScheduledTaskSettingsSet `
        -AllowStartIfOnBatteries `
        -DontStopIfGoingOnBatteries `
        -StartWhenAvailable `
        -RunOnlyIfNetworkAvailable `
        -DontStopOnIdleEnd `
        -RestartInterval (New-TimeSpan -Minutes 15) `
        -RestartCount 3
    
    # Utwórz principal (z jakimi uprawnieniami)
    $Principal = New-ScheduledTaskPrincipal `
        -UserId "SYSTEM" `
        -LogonType ServiceAccount `
        -RunLevel Highest
    
    # Zarejestruj zadanie
    Register-ScheduledTask `
        -TaskName $TaskName `
        -Description $TaskDescription `
        -Action $Action `
        -Trigger $Trigger `
        -Settings $Settings `
        -Principal $Principal `
        -Force
    
    Write-Host "✓ Zadanie '$TaskName' zostało utworzone!" -ForegroundColor Green
    Write-Host "  Trigger: Codziennie o $TriggerTime" -ForegroundColor Cyan
    Write-Host "  Script: $ScriptPath" -ForegroundColor Cyan

### Uruchomienie

Otwórz **PowerShell jako Administrator**:

1. Win + X → **Windows PowerShell (Admin)**
2. Przejdź do folderu:

    cd C:\Users\YourUsername\my-it-profile-hub\Automation-Scripts\Infrastructure-Docs-Generator

3. Uruchom skrypt:

    .\create_scheduled_task.ps1

Jeśli zobaczysz błąd "execution policy", uruchom najpierw:

    Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy Bypass -Force

---

## 🧪 Testowanie Zadania

### Test 1: Ręczne Uruchomienie z Task Scheduler

1. Otwórz Task Scheduler (`taskschd.msc`)
2. Znajdź zadanie: **Infrastructure Documentation Generator**
3. Kliknij prawym → **Run**
4. Sprawdź status w kolumnie **Last Run Result**

Powinno być: **The operation completed successfully (0x0)**

### Test 2: Sprawdzenie Logów

Otwórz plik:

    output\logs\scheduler.log

Powinieneś zobaczyć:

    [2026-01-28 14:30:15] Uruchamiam Infrastructure Documentation Generator...
    ======================================================================
       Infrastructure Documentation Generator
    ======================================================================
    ...
    [2026-01-28 14:35:42] Zakończono z kodem: 0

**Kod 0** = Sukces

### Test 3: Sprawdzenie Historii Zadania

W Task Scheduler:

1. Znajdź zadanie
2. Kliknij prawym → **Properties**
3. Zakładka **History** (dolna część okna)

Zobaczysz wszystkie uruchomienia z kodami błędów (jeśli były).

### Test 4: Sprawdzenie Wygenerowanych Plików

Sprawdź czy pojawiły się nowe pliki:

    output\network-docs\
    output\raw-configs\

---

## 🔧 Rozwiązywanie Problemów

### Problem 1: Zadanie nie uruchamia się

**Sprawdź:**

1. **Trigger jest włączony?**
   - Task Scheduler → Zadanie → Properties → Triggers → Sprawdź checkbox "Enabled"

2. **Zadanie nie jest wyłączone?**
   - Task Scheduler → Zadanie → Prawy klik → "Enable" (jeśli szare, jest włączone)

3. **Status w History:**
   - Task Scheduler → Zadanie → History (dolna część)
   - Szukaj Event ID 103 (uruchomienie) i 102 (błąd)

### Problem 2: Zadanie uruchamia się, ale nic nie robi

**Sprawdź:**

1. **Ścieżka do pliku batch jest poprawna:**

   - Otwórz `run_generator.bat` w Notatniku
   - Sprawdź czy ścieżka w linii `cd /d ...` jest prawidłowa

2. **Virtual environment istnieje:**

   - Sprawdź czy folder `venv\` istnieje w projekcie

3. **Logi scheduler.log:**

   - Otwórz `output\logs\scheduler.log`
   - Sprawdź ostatnie wpisy

### Problem 3: Last Run Result = 0x1 (błąd)

**Kod 0x1** oznacza ogólny błąd. Sprawdź:

1. **Logi Python:**

   - `output\logs\collector.log`
   - `output\logs\generator.log`
   - `output\logs\scheduler.log`

2. **Test ręczny:**

   - Uruchom `run_generator.bat` ręcznie (podwójne kliknięcie)
   - Zobacz błędy w oknie CMD

### Problem 4: Zadanie wymaga logowania użytkownika

**Objaw:** Zadanie działa tylko gdy jesteś zalogowany

**Rozwiązanie:**

1. Task Scheduler → Zadanie → Properties → General
2. Zaznacz: **Run whether user is logged on or not**
3. Kliknij OK → Podaj hasło administratora

### Problem 5: "The operator or administrator has refused the request (0x800710E0)"

**Przyczyna:** Zadanie jest wyłączone lub zablokowane przez politykę

**Rozwiązanie:**

1. Sprawdź czy zadanie jest włączone:
   - Zadanie → Prawy klik → Enable

2. Sprawdź Group Policy (jeśli w domenie):
   - Win + R → `gpedit.msc`
   - Computer Configuration → Windows Settings → Security Settings → Local Policies → User Rights Assignment
   - "Log on as a batch job" - dodaj swoje konto

### Problem 6: Zadanie nie budzi komputera ze sleep

**Rozwiązanie:**

1. Task Scheduler → Zadanie → Properties → Conditions
2. Zaznacz: **Wake the computer to run this task**
3. Windows Settings → System → Power & Sleep → Additional power settings
4. Change plan settings → Change advanced power settings
5. Sleep → Allow wake timers → Enable

---

## ✅ Best Practices

### 1. Logowanie

**Zawsze loguj output do pliku:**

W `run_generator.bat` dodaj przekierowanie:

    python scripts\main.py >> output\logs\scheduler.log 2>&1

`2>&1` przekierowuje również błędy (stderr) do logów.

### 2. Email Notifications

**Dodaj wysyłanie emaila po zakończeniu:**

Na końcu `run_generator.bat` dodaj:

    REM Wyślij email po zakończeniu
    if %EXIT_CODE% NEQ 0 (
        powershell -Command "Send-MailMessage -To 'admin@firma.pl' -From 'scheduler@firma.pl' -Subject 'Infrastructure Docs - BŁĄD' -Body 'Sprawdź logi!' -SmtpServer 'smtp.firma.pl'"
    )

### 3. Retry przy Błędzie

W Task Scheduler → Settings:

- Zaznacz: **If the task fails, restart every: 15 minutes**
- **Attempt to restart up to: 3 times**

### 4. Monitoring

**Utwórz osobne zadanie które sprawdza czy główne zadanie działa:**

    # check_task.ps1
    $LastRun = (Get-ScheduledTask -TaskName "Infrastructure Documentation Generator").LastRunTime
    $Now = Get-Date
    $Diff = ($Now - $LastRun).TotalHours
    
    if ($Diff -gt 25) {
        Send-MailMessage -To "admin@firma.pl" -Subject "ALERT: Task nie uruchomił się!" -Body "Sprawdź Task Scheduler"
    }

Zaplanuj na 3:00 (godzinę po głównym zadaniu).

### 5. Backup Logów

Automatyczne archiwizowanie starych logów:

    REM Na początku run_generator.bat
    if exist output\logs\scheduler.log (
        if %DATE:~6,4%-%DATE:~3,2%-%DATE:~0,2% == Poniedziałek (
            move output\logs\scheduler.log output\logs\scheduler_%DATE:~6,4%-%DATE:~3,2%-%DATE:~0,2%.log
        )
    )

---

## 📊 Przykładowy Harmonogram

**Zalecany harmonogram dla różnych środowisk:**

### Małe Biuro (do 20 urządzeń)

- **Częstotliwość:** Codziennie o 2:00 AM
- **Retry:** 3 razy co 15 minut

### Średnia Firma (20-100 urządzeń)

- **Częstotliwość:** Codziennie o 1:00 AM (wcześniej, bo dłużej trwa)
- **Dodatkowy trigger:** W weekend o 12:00 (backup)
- **Retry:** 5 razy co 10 minut

### Duża Korporacja (100+ urządzeń)

- **Częstotliwość:** Dwa razy dziennie (1:00 AM i 1:00 PM)
- **Segmentacja:** Różne zadania dla różnych lokalizacji
- **Monitoring:** Osobne zadanie sprawdzające status co godzinę

---

## 📝 Checklist Konfiguracji

Przed finalizacją, sprawdź:

- [ ] Plik `run_generator.bat` jest utworzony i przetestowany ręcznie
- [ ] Ścieżki w pliku batch są poprawne (absolutne, nie relatywne)
- [ ] Zadanie w Task Scheduler jest utworzone
- [ ] Trigger ustawiony na codziennie o 2:00 AM
- [ ] "Run whether user is logged on or not" jest zaznaczone
- [ ] "Run with highest privileges" jest zaznaczone
- [ ] "Wake computer to run this task" jest zaznaczone (jeśli laptop)
- [ ] Retry policy ustawiony (3 razy co 15 minut)
- [ ] Ręczne uruchomienie działa (Run → sprawdź Last Run Result = 0x0)
- [ ] Logi są tworzone (`output\logs\scheduler.log`)
- [ ] Pliki są generowane (`output\network-docs\`)

---

**Data aktualizacji:** 2026-01-28  
**Wersja:** 1.0
