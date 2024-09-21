# Web Scraping Condominium Rental in Kuala Lumpur

**Objective**: The objective of this project is to scrape condominium rental in Kuala Lumpur from Mudah (www.mudah.my/kuala-lumpur/apartment-condominium-for-rent) and export the average size and average rental(RM) for each property in different areas in CSV format.

## Steps

* Beautiful Soup primarily works with static content—HTML and XML documents as they are loaded in the browser. 
* For dynamic websites such as Mudah.com that use JavaScript to load content, 
* Beautiful Soup alone is not sufficient because it cannot execute JavaScript.
* Therefore, we use Selenium library in Python to load dynamic content from Mudah.com.
* We can see that the listing page on Mudah.com contains Property type, no of Bedrooms, no of Bathrooms, Pricing, Area, and the listing datetime. 
* One thing to note is that the property name is not shown on the listing page. We need to click on the link to get the details about the Property.
* So, in this case we scrape the Pricing, Size, Area on the listing page, and the Property name on the details page.
* The first step of scrapping is to identify the tag that contains the information that we want to scrap
* We cannot directly use the class name as this is dynamic web. The class name changes when we refresh the web.
* From the html code we can see that the all the listing tags have an attribute called ‘data-testid’, and they contain substrings ‘listing-ad-item’. We can make use of this characteristics to scrape the information for each property listed on the page.
* Within the listing tag, we find the tag that contains the link of the details page **<a href=“”>**, and then scrape the Property name information from it.
* On the property details page, we identify the tag that contains property information and define a function to extract the property name.
* After getting all the information we want, we store it into a list then append to pandas dataframe for further processing。
* We do a little pre-processing stuff to clean the data by removing the non-numeric characters and commas, making it suitable for analysis.
* After that, we use ‘groupby’ function in Pandas library to calculate the average price and size for each property, then convert the dataframe to excel.
