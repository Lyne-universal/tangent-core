#!/usr/bin/env python3
"""Lyne Universal Systems // Tangent Desktop App
A modern, local-first GUI for the Tangent Security Engine
"""

import os
import tkinter as tk
from tkinter import filedialog

import customtkinter as ctk  # type: ignore

from tangent_core import TangentEngine

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class TangentApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.engine = TangentEngine()

        self.title("✦ LYNE UNIVERSAL SYSTEMS // TANGENT DASHBOARD")
        self.geometry("900x550")
        self.resizable(False, False)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(1, weight=1)

        self.header = ctk.CTkFrame(self, height=60, corner_radius=0)
        self.header.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)

        self.title_label = ctk.CTkLabel(
            self.header,
            text="TANGENT SECURE SCRUBBER",
            font=ctk.CTkFont(size=18, weight="bold"),
        )
        self.title_label.pack(side="left", padx=20)

        self.browse_btn = ctk.CTkButton(self.header, text="Select Target File", command=self.select_file)
        self.browse_btn.pack(side="right", padx=20)

        self.left_panel = ctk.CTkFrame(self, width=280)
        self.left_panel.grid(row=1, column=0, sticky="nsew", padx=(10, 5), pady=(0, 10))

        self.meta_title = ctk.CTkLabel(self.left_panel, text="AUDIT COUNTERMEASURES", font=ctk.CTkFont(size=14, weight="bold"))
        self.meta_title.pack(pady=15)

        self.status_lbl = ctk.CTkLabel(self.left_panel, text="Engine Status: IDLE", text_color="gray")
        self.status_lbl.pack(pady=10)

        self.lines_lbl = ctk.CTkLabel(self.left_panel, text="Lines Processed: 0")
        self.lines_lbl.pack(pady=10)

        self.vuln_lbl = ctk.CTkLabel(self.left_panel, text="Leaks Neutralized: 0", font=ctk.CTkFont(weight="bold"))
        self.vuln_lbl.pack(pady=10)

        self.save_btn = ctk.CTkButton(self.left_panel, text="Export Safe Copy", state="disabled", command=self.export_file)
        self.save_btn.pack(side="bottom", pady=20)

        self.right_panel = ctk.CTkFrame(self)
        self.right_panel.grid(row=1, column=1, sticky="nsew", padx=(5, 10), pady=(0, 10))

        self.preview_lbl = ctk.CTkLabel(self.right_panel, text="SANITIZED STREAM PREVIEW", font=ctk.CTkFont(size=12, weight="bold"))
        self.preview_lbl.pack(pady=10)

        self.text_preview = ctk.CTkTextbox(self.right_panel, font=ctk.CTkFont(family="Courier", size=12))
        self.text_preview.pack(expand=True, fill="both", padx=15, pady=(0, 15))
        self.text_preview.insert("0.0", "# Select a file above to view the redacted data stream preview...")
        self.text_preview.configure(state="disabled")

        self.active_file_path: str = ""
        self.scrubbed_content_cache: str = ""

    def select_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text/Log Files", "*.log *.txt *.env *.json")])
        if file_path:
            self.active_file_path = file_path
            self.run_engine_analysis()

    def run_engine_analysis(self):
        if not self.active_file_path:
            return

        # Scan + redact file to a safe output copy
        output_temp = f"{os.path.splitext(self.active_file_path)[0]}.temp"
        report = self.engine.process_file(self.active_file_path, output_temp)


        if report["engine_status"] == "COMPLETED":
            self.status_lbl.configure(text="Engine Status: ACTIVE", text_color="#10B981")
            self.lines_lbl.configure(text=f"Lines Processed: {report['metrics']['lines_processed']}")

            vulns = report["metrics"]["vulnerabilities_neutralized"]

            vuln_color = "#EF4444" if vulns > 0 else "#10B981"
            self.vuln_lbl.configure(text=f"Leaks Neutralized: {vulns}", text_color=vuln_color)

            self.scrubbed_content_cache = json.dumps(report, indent=2)

            self.text_preview.configure(state="normal")
            self.text_preview.delete("0.0", "end")
            self.text_preview.insert("0.0", self.scrubbed_content_cache)
            self.text_preview.configure(state="disabled")

            self.save_btn.configure(state="normal")

    def export_file(self):
        if self.scrubbed_content_cache and self.active_file_path:
            save_path = filedialog.asksaveasfilename(
                defaultextension=".log",
                filetypes=[("Log File", "*.log"), ("Text File", "*.txt"), ("Env Configuration File", "*.env")],
                initialfile=f"{os.path.basename(os.path.splitext(self.active_file_path)[0])}.scrubbed",
            )
            if save_path:
                with open(save_path, "w", encoding="utf-8") as f:
                    f.write(self.scrubbed_content_cache)
                self.status_lbl.configure(text="EXPORT COMPLETED Successfully!", text_color="#3B82F6")


if __name__ == "__main__":
    import json

    app = TangentApp()
    app.mainloop()

