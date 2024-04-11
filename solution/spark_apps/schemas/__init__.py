#schemas v1

from pyspark.sql import types

customers_schema = types.StructType(
    [
        types.StructField("Customer ID", types.IntegerType(), False),
        types.StructField("Last Used Platform", types.StringType(), True),
        types.StructField("Is Blocked", types.ByteType(), True),
        types.StructField("Created At", types.TimestampType(), False),
        types.StructField("Language", types.StringType(), True),
        types.StructField("Outstanding Amount", types.FloatType(), True),
        types.StructField("Loyalty Points", types.IntegerType(), True),
        types.StructField("Number of Employees", types.IntegerType(), True),
    ]
)

deliveries_schema = types.StructType(
    [
        types.StructField("Task_ID", types.IntegerType(), False),
        types.StructField("Order_ID", types.StringType(), False),
        types.StructField("Relationship", types.StringType(), True),
        types.StructField("Team_Name", types.StringType(), True),
        types.StructField("Task_Type", types.StringType(), True),
        types.StructField("Notes", types.StringType(), True),
        types.StructField("Agent_ID", types.IntegerType(), True),
        types.StructField("Distance(m)", types.FloatType(), True),
        types.StructField("Total_Time_Taken(min)", types.FloatType(), True),
        types.StructField("Task_Status", types.StringType(), True),
        types.StructField("Ref_Images", types.StringType(), True),
        types.StructField("Rating", types.FloatType(), True),
        types.StructField("Review", types.StringType(), True),
        types.StructField("Latitude", types.FloatType(), True),
        types.StructField("Longitude", types.FloatType(), True),
        types.StructField("Tags", types.StringType(), True),
        types.StructField("Promo_Applied", types.StringType(), True),
        types.StructField("Custom_Template_ID", types.StringType(), True),
        types.StructField("Task_Details_QTY", types.IntegerType(), True),
        types.StructField("Task_Details_AMOUNT", types.FloatType(), True),
        types.StructField("Special_Instructions", types.StringType(), True),
        types.StructField("Tip", types.StringType(), True),
        types.StructField("Delivery_Charges", types.StringType(), True),
        types.StructField("Discount", types.StringType(), True),
        types.StructField("Subtotal", types.FloatType(), True),
        types.StructField("Payment_Type", types.StringType(), True),
        types.StructField("Task_Category", types.StringType(), True),
        types.StructField("Earning", types.FloatType(), True),
        types.StructField("Pricing", types.StringType(), True),
    ]
)

orders_schema = types.StructType(
    [
        types.StructField("Order ID", types.IntegerType(), False),
        types.StructField("Order Status", types.StringType(), True),
        types.StructField("Category Name", types.StringType(), True),
        types.StructField("SKU", types.StringType(), True),
        types.StructField("Customization Group", types.StringType(), True),
        types.StructField("Customization Option", types.StringType(), True),
        types.StructField("Quantity", types.IntegerType(), True),
        types.StructField("Unit Price", types.FloatType(), True),
        types.StructField("Cost Price", types.FloatType(), True),
        types.StructField("Total Cost Price", types.FloatType(), True),
        types.StructField("Total Price", types.FloatType(), True),
        types.StructField("Order Total", types.FloatType(), True),
        types.StructField("Sub Total", types.FloatType(), True),
        types.StructField("Tax", types.FloatType(), True),
        types.StructField("Delivery Charge", types.FloatType(), True),
        types.StructField("Tip", types.FloatType(), True),
        types.StructField("Discount", types.FloatType(), True),
        types.StructField("Remaining Balance", types.FloatType(), True),
        types.StructField("Payment Method", types.StringType(), True),
        types.StructField("Additional Charge", types.FloatType(), True),
        types.StructField("Taxable Amount", types.FloatType(), True),
        types.StructField("Transaction ID", types.StringType(), True),
        types.StructField("Currency Symbol", types.StringType(), True),
        types.StructField("Transaction Status", types.StringType(), True),
        types.StructField("Promo Code", types.StringType(), True),
        types.StructField("Customer ID", types.IntegerType(), True),
        types.StructField("Merchant ID", types.IntegerType(), True),
        types.StructField("Description", types.StringType(), True),
        types.StructField("Distance (in km)", types.FloatType(), True),
        types.StructField("Order Time", types.TimestampType(), True),
        types.StructField("Pickup Time", types.TimestampType(), True),
        types.StructField("Delivery Time", types.TimestampType(), True),
        types.StructField("Ratings", types.FloatType(), True),
        types.StructField("Reviews", types.StringType(), True),
        types.StructField("Merchant Earning", types.FloatType(), True),
        types.StructField("Commission Amount", types.FloatType(), True),
        types.StructField("Commission Payout Status", types.StringType(), True),
        types.StructField("Order Preparation Time", types.FloatType(), True),
        types.StructField("Redeemed Loyalty Points", types.IntegerType(), True),
        types.StructField("Consumed Loyalty Points", types.IntegerType(), True),
        types.StructField("Cancellation Reason", types.StringType(), True),
        types.StructField("Flat Discount", types.FloatType(), True),
        types.StructField("Checkout Template Name", types.StringType(), True),
        types.StructField("Checkout Template Value", types.StringType(), True),
    ]
)
