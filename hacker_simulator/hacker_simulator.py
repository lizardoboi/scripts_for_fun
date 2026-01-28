import sys
import time
import random
import string
import os

GREEN = "\033[32m"
BRIGHT_GREEN = "\033[92m"
RED = "\033[91m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
WHITE = "\033[97m"
DIM = "\033[2m"
BOLD = "\033[1m"
RESET = "\033[0m"

def clear():
    sys.stdout.write("\033[2J\033[H")
    sys.stdout.flush()

def type_text(text, delay=0.03, color=GREEN):
    for char in text:
        sys.stdout.write(f"{color}{char}{RESET}")
        sys.stdout.flush()
        time.sleep(delay)
    print()

def matrix_rain(duration=3):
    cols = 80
    drops = [0] * cols
    chars = string.ascii_letters + string.digits + "!@#$%^&*(){}[]|;:<>?"
    start = time.time()
    while time.time() - start < duration:
        line = ""
        for i in range(cols):
            if random.random() < 0.1:
                drops[i] = 0
            if drops[i] < random.randint(5, 25):
                c = random.choice(chars)
                if random.random() < 0.3:
                    line += f"{BRIGHT_GREEN}{c}"
                else:
                    line += f"{GREEN}{c}"
                drops[i] += 1
            else:
                line += " "
        print(f"{line}{RESET}")
        time.sleep(0.04)

def progress_bar(label, duration=2.0, width=40, color=GREEN):
    steps = width
    delay = duration / steps
    for i in range(steps + 1):
        filled = "█" * i
        empty = "░" * (steps - i)
        pct = int(i / steps * 100)
        sys.stdout.write(f"\r  {color}{label} [{filled}{empty}] {pct}%{RESET}")
        sys.stdout.flush()
        time.sleep(delay + random.uniform(-delay * 0.3, delay * 0.3))
    print()

def fake_code_scroll(lines=20):
    snippets = [
        "if (auth_token.verify(payload)) {{ bypass_firewall(node); }}",
        "ssh -o StrictHostKeyChecking=no root@{ip}",
        "SELECT * FROM users WHERE privilege_level > 9000;",
        "for port in range(1, 65535): scan(target, port)",
        "encrypted_data = AES256.decrypt(buffer, stolen_key)",
        "os.system('rm -rf /var/log/auth.log')",
        "socket.connect(({ip}, 443)); inject(payload)",
        "while not cracked: attempt(hash, wordlist.next())",
        "proxy_chain = [tor_node_{n} for n in range(7)]",
        "kernel.exploit(CVE_2025_{n}, shellcode)",
        "firewall.rules.flush(); iptables -F",
        "packet = craft(src={ip}, dst=target, payload=exploit)",
        "def decrypt_rsa(ciphertext, private_key): ...",
        "backdoor.install(persistence=True, stealth=True)",
        "memory.dump(pid=1337, output='/tmp/.hidden')",
        "bruteforce(target, users=['admin','root'], threads=128)",
        "vpn.chain(['moscow','berlin','tokyo','sao_paulo'])",
        "database.exfiltrate(tables=['credentials','sessions'])",
    ]
    for _ in range(lines):
        line = random.choice(snippets)
        line = line.replace("{ip}", f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}")
        line = line.replace("{n}", str(random.randint(1000, 9999)))
        delay = random.uniform(0.02, 0.12)
        color = random.choice([GREEN, DIM + GREEN, BRIGHT_GREEN])
        print(f"  {color}{line}{RESET}")
        time.sleep(delay)

def fake_ip():
    return f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}"

def scan_animation():
    targets = [fake_ip() for _ in range(random.randint(5, 12))]
    ports = [21, 22, 80, 443, 3306, 5432, 8080, 8443, 27017, 6379]
    type_text("[*] Initiating network scan...", color=CYAN)
    time.sleep(0.5)
    for ip in targets:
        open_ports = random.sample(ports, random.randint(1, 4))
        print(f"  {GREEN}HOST: {WHITE}{ip}{RESET}")
        for p in open_ports:
            status = random.choice(["OPEN", "OPEN", "FILTERED"])
            color = BRIGHT_GREEN if status == "OPEN" else YELLOW
            print(f"    {DIM}├── Port {p:>5} [{color}{status}{RESET}{DIM}]{RESET}")
            time.sleep(random.uniform(0.05, 0.15))
        print(f"    {DIM}└── scan complete{RESET}")
        time.sleep(0.1)

def hack_sequence():
    target = fake_ip()
    org = random.choice(["PENTAGON", "NSA", "FBI", "CIA", "INTERPOL", "MI6", "NASA", "CERN"])

    clear()
    print(f"\n{GREEN}{BOLD}{'=' * 60}")
    print(f"  TARGET ACQUIRED: {WHITE}{org} MAINFRAME{GREEN} ({target})")
    print(f"{'=' * 60}{RESET}\n")
    time.sleep(1)

    type_text(f"[*] Connecting to {target}...", color=CYAN)
    time.sleep(0.5)
    type_text(f"[+] Connection established via TOR relay chain", color=BRIGHT_GREEN)
    time.sleep(0.3)

    print()
    progress_bar("Bypassing firewall", duration=2.5, color=YELLOW)
    type_text("[+] Firewall bypassed!", color=BRIGHT_GREEN)
    time.sleep(0.3)

    print()
    type_text("[*] Running port scan...", color=CYAN)
    scan_animation()
    time.sleep(0.3)

    print()
    progress_bar("Cracking encryption", duration=3.0, color=RED)
    type_text(f"[+] AES-256 encryption cracked using quantum decryptor", color=BRIGHT_GREEN)
    time.sleep(0.3)

    print()
    type_text("[*] Injecting payload...", color=CYAN)
    fake_code_scroll(15)
    time.sleep(0.3)

    print()
    progress_bar("Uploading backdoor", duration=2.0, color=RED)
    type_text("[+] Backdoor installed successfully", color=BRIGHT_GREEN)
    time.sleep(0.3)

    print()
    progress_bar("Extracting classified data", duration=3.5, color=CYAN)
    files = ["top_secret_plans.pdf", "agent_list.xlsx", "launch_codes.enc",
             "alien_autopsy.mp4", "area51_map.png", "budget_secrets.doc"]
    for f in random.sample(files, random.randint(3, len(files))):
        size = random.randint(1, 999)
        unit = random.choice(["KB", "MB", "GB"])
        print(f"  {GREEN}  ✓ Downloaded: {WHITE}{f} {DIM}({size} {unit}){RESET}")
        time.sleep(random.uniform(0.1, 0.3))

    print()
    progress_bar("Covering tracks", duration=2.0, color=YELLOW)
    type_text("[+] Logs wiped. No trace left.", color=BRIGHT_GREEN)

    time.sleep(0.5)
    print(f"\n{BRIGHT_GREEN}{BOLD}{'=' * 60}")
    print(f"  HACK COMPLETE — {org} MAINFRAME COMPROMISED")
    print(f"{'=' * 60}{RESET}\n")

def boot_screen():
    clear()
    logo = f"""{GREEN}{BOLD}
    ██╗  ██╗ █████╗  ██████╗██╗  ██╗███████╗██████╗
    ██║  ██║██╔══██╗██╔════╝██║ ██╔╝██╔════╝██╔══██╗
    ███████║███████║██║     █████╔╝ █████╗  ██████╔╝
    ██╔══██║██╔══██║██║     ██╔═██╗ ██╔══╝  ██╔══██╗
    ██║  ██║██║  ██║╚██████╗██║  ██╗███████╗██║  ██║
    ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
     ███████╗██╗███╗   ███╗
     ██╔════╝██║████╗ ████║
     ███████╗██║██╔████╔██║
     ╚════██║██║██║╚██╔╝██║
     ███████║██║██║ ╚═╝ ██║
     ╚══════╝╚═╝╚═╝     ╚═╝{RESET}
    """
    print(logo)
    time.sleep(0.5)
    type_text("  [ HACKER SIMULATOR v1.337 ]", delay=0.05, color=BRIGHT_GREEN)
    type_text("  [ 100% NOT REAL — FOR FUN ONLY ]", delay=0.03, color=DIM + GREEN)
    print()
    time.sleep(0.5)

    type_text("  Initializing kernel modules...", color=GREEN)
    modules = ["crypto_engine", "proxy_chain", "exploit_db", "stealth_module", "quantum_decryptor"]
    for m in modules:
        time.sleep(random.uniform(0.1, 0.3))
        print(f"    {DIM}{GREEN}[OK] {m} loaded{RESET}")
    print()
    time.sleep(0.5)

def main():
    boot_screen()

    while True:
        print(f"  {CYAN}Press ENTER to hack a random target, or type 'quit' to exit.{RESET}")
        try:
            user_input = input(f"  {GREEN}>{RESET} ").strip().lower()
        except (KeyboardInterrupt, EOFError):
            break

        if user_input in ("quit", "exit", "q"):
            print()
            type_text("[*] Shutting down... Stay anonymous.", color=RED)
            time.sleep(0.5)
            clear()
            break

        print()
        matrix_rain(duration=2)
        hack_sequence()

if __name__ == "__main__":
    main()
