### Google Sheets parser

*For parsing my bake shop orders from Google Forms*

---
A simple spreadsheet parser that is integrated with the Google Sheets API to allow seamless parsing of data without having to first manually export the csv file from Google Sheets. It is built using the [starter code](https://developers.google.com/sheets/api/quickstart/python) provided by the Google Sheets API. 

This parser processes the orders I collect using Google Forms for the sales of my millionaire shortbread (see [my Instagram](https://www.instagram.com/brd_n_bttr/) for details). Specifically, it calculates the total cost for each customer while accounting for the different delivery methods, and tabulates the total number of shortbread from each flavour across all orders. As each order can contain any mix of flavours as selected by the customer, this parser completely eliminates any human error I may potentially make in compiling the orders, and ensures that all customers will receive the correct flavour.

