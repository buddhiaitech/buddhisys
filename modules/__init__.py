"""
RPA Modules Package
Contains all automation modules for the RPA workflow
"""

__version__ = "1.0.0"
__author__ = "RPA System"

from .browser_automation import BrowserAutomation
from .pdf_processor import PDFProcessor
from .email_automation import EmailAutomation

__all__ = [
    'BrowserAutomation',
    'PDFProcessor', 
    'EmailAutomation'
]




