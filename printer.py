import socket
import datetime
import os
import subprocess

def convert_ps_to_pdf(ps_filename):
    """Converts the PostScript file to a PDF using a sandboxed Ghostscript process."""
    pdf_filename = ps_filename.replace('.ps', '.pdf')
    print(f"[*] Converting to PDF: {pdf_filename}")
    
    try:
        subprocess.run([
            'gs', 
            '-dSAFER',       # CRITICAL: Sandbox mode prevents OS command execution and arbitrary file access
            '-dNOPAUSE', 
            '-dBATCH', 
            '-sDEVICE=pdfwrite', 
            f'-sOutputFile={pdf_filename}', 
            ps_filename
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        print(f"[✓] Success! PDF saved: {os.path.basename(pdf_filename)}")
        
        # Clean up the raw .ps file to save space
        if os.path.exists(ps_filename):
            os.remove(ps_filename)
            
    except subprocess.CalledProcessError:
        print("[!] Ghostscript error during conversion.")

def start_server(host='0.0.0.0', port=9100, output_dir='/app/print_jobs'):
    """Starts the TCP socket server to catch HP Jetdirect print jobs."""
    os.makedirs(output_dir, exist_ok=True)
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))
        s.listen()
        
        print("="*50)
        print(f"[*] Secure Virtual Printer listening on {host}:{port}")
        print("="*50)
        
        while True:
            conn, addr = s.accept()
            with conn:
                print(f"\n[+] Incoming print job received from {addr}")
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                ps_filename = f"{output_dir}/job_{timestamp}.ps"
                
                # Catch the raw print data stream
                with open(ps_filename, "wb") as f:
                    while True:
                        data = conn.recv(4096)
                        if not data:
                            break
                        f.write(data)
                
                print(f"[+] Raw print job saved. Triggering conversion...")
                convert_ps_to_pdf(ps_filename)

if __name__ == '__main__':
    try:
        start_server()
    except KeyboardInterrupt:
        print("\n[*] Shutting down virtual printer.")
