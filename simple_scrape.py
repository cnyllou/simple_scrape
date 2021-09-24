from urlextract import URLExtract
from email_scraper import scrape_emails
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from uuid import uuid4

from phonenumbers import (
    format_number, PhoneNumberMatcher, PhoneNumberFormat
)

import argparse
import requests


class PhoneNumber(BaseModel):
    country_code: str
    number: str
    string: str


class Link(BaseModel):
    url: str


class Email(BaseModel):
    string: str
    # domain: str
    # host: str
    # tld: str


class Report(BaseModel):
    parsing_datetime: datetime

    id: str = str(uuid4())
    emails: Optional[list[Email]] = list()
    phone_numbers: Optional[list[PhoneNumber]] = list()
    links: Optional[list[Link]] = list()

    def print_phone_numbers(self):
        if not self.phone_numbers:
            print("No phone numbers were found.")
            return None

        for obj in self.phone_numbers:
            print(obj.string)

    def print_emails(self):
        if not self.emails:
            print("No emails were found.")
            return None

        for obj in self.emails:
            print(obj.string)

    def print_links(self):
        if not self.links:
            print("No links were found.")
            return None

        for obj in self.links:
            print(obj)


class Parser:
    """Class representing the text parser"""

    def parse_text(self, text) -> None:
        """Parse given text and store results"""
        self.phone_numbers = self.parse_phone_numbers(text)
        self.emails = self.parse_emails(text)
        self.links = self.parse_links(text)

    def generate_report(self) -> Report:
        """Generate a report object and return it"""
        return Report(
            parsing_datetime=datetime.now(),
            phone_numbers=self.phone_numbers,
            emails=self.emails,
            links=self.links)

    def parse_phone_numbers(self, text) -> list[PhoneNumber]:
        """Parse phone numbers from given text"""
        return [PhoneNumber(
            country_code=match.number.country_code_source,
            number=match.number.national_number,
            string=format_number(
                match.number,
                PhoneNumberFormat.NATIONAL
            )
        ) for match in PhoneNumberMatcher(text, "LV")]

    def parse_emails(self, text) -> list[Email]:
        email_set = scrape_emails(text)
        return [Email(string=email)
                for email in email_set]

    def parse_links(self, text) -> list[Link]:
        extractor = URLExtract()
        links = extractor.find_urls(text)
        return [Link(url=link)
                for link in links]


def parse_args():
    parser = argparse.ArgumentParser("Url parser")
    parser.add_argument("url")
    return parser.parse_args()


def main():
    url = args.url
    text = requests.get(url).text
    parser = Parser()
    parser.parse_text(text)
    report = parser.generate_report()

    print("\n*** PHONE NUMBERS ***")
    report.print_phone_numbers()
    print("\n*** EMAILS ***")
    report.print_emails()
    print("\n*** LINKS ***")
    report.print_links()


if __name__ == "__main__":
    args = parse_args()
    main()
