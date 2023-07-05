import stripe
from rest_framework import serializers

from Library_service import settings
from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"


class PaymentCreateSerializer(PaymentSerializer):
    class Meta:
        model = Payment
        fields = "__all__"
        read_only_fields = (
            "status",
            "type",
            "session_url",
            "session_id",
            "money_to_pay",
        )

    def get_money_to_pay(self):
        book = self.validated_data["borrowing"].book
        borrowing = self.validated_data["borrowing"]
        borrow_date = borrowing.borrow_date
        expected_return_date = borrowing.expected_return_date

        days_borrowed = (expected_return_date - borrow_date).days
        money_to_pay = book.daily_fee * days_borrowed

        return money_to_pay

    def create(self, validated_data):
        stripe.api_key = settings.STRIPE_SECRET_KEY

        validated_data["money_to_pay"] = self.get_money_to_pay()

        instance = super().create(validated_data)

        print(validated_data)

        payment_response = stripe.checkout.Session.create(
            payment_method_types=["card"],
            success_url="http://127.0.0.1:8000/api/payments/success/{}".format(
                instance.id
            ),
            cancel_url="http://127.0.0.1:8000/api/payments/cancel/{}".format(
                instance.id
            ),
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "product_data": {
                            "name": instance.borrowing.book.title,
                        },
                        "unit_amount": int(validated_data["money_to_pay"] * 100),
                    },
                    "quantity": 1,
                }
            ],
            mode="payment",
        )

        instance.session_id = payment_response["id"]
        instance.session_url = payment_response["url"]
        instance.save()

        return instance


class PaymentSuccessSerializer(PaymentSerializer):
    class Meta:
        model = Payment
        fields = ("status",)


class PaymentCancelSerializer(PaymentSerializer):
    class Meta:
        model = Payment
        fields = ("status",)
