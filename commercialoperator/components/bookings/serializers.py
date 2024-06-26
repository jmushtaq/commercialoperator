from django.conf import settings
from django.utils import timezone
from ledger.accounts.models import EmailUser,Address
from ledger.payments.invoice.models import Invoice
from commercialoperator.components.proposals.serializers import ProposalSerializer, InternalProposalSerializer, ProposalParkSerializer
from commercialoperator.components.main.serializers import ApplicationTypeSerializer
from commercialoperator.components.bookings.models import (
    Booking,
    ParkBooking,
    BookingInvoice,
)
from commercialoperator.components.proposals.serializers import ProposalSerializer
from rest_framework import serializers


class BookingInvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingInvoice
        fields = 'invoice_reference'


class ParkBookingSerializer(serializers.ModelSerializer):
    park = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = ParkBooking
        fields = (
            'id',
            'park',
            'arrival',
            'no_adults',
            'no_children',
            'no_free_of_charge',
            'cost',
        )
        datatables_always_serialize = (
            'id',
            'park',
            'arrival',
            'no_adults',
            'no_children',
            'no_free_of_charge',
            'cost',
        )

    def get_park(self,obj):
        return obj.park.name


class BookingSerializer(serializers.ModelSerializer):
    park_bookings = ParkBookingSerializer(many=True, read_only=True)
    application_fee_invoice = serializers.SerializerMethodField(read_only=True)
    approval_number = serializers.SerializerMethodField(read_only=True)
    applicant = serializers.SerializerMethodField(read_only=True)
    org_applicant = serializers.SerializerMethodField(read_only=True)
    trading_name = serializers.SerializerMethodField(read_only=True)
    proxy_applicant = serializers.SerializerMethodField(read_only=True)
    payment_status = serializers.SerializerMethodField(read_only=True)
    payment_method = serializers.SerializerMethodField(read_only=True)
    invoice_reference = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Booking
        fields = (
            'id',
            'admission_number',
            'application_fee_invoice',
            'approval_number',
            'applicant',
            'org_applicant',
            'trading_name',
            'proxy_applicant',
            'payment_status',
            'payment_method',
            'invoice_reference',
            'park_bookings',
        )
        datatables_always_serialize = (
            'id',
            'admission_number',
            'application_fee_invoice',
            'approval_number',
            'applicant',
            'org_applicant',
            'trading_name',
            'proxy_applicant',
            'payment_status',
            'payment_method',
            'invoice_reference',
            'park_bookings',
        )

    def get_application_fee_invoice(self,obj):
        return obj.proposal.fee_invoice_reference

    def get_approval_number(self,obj):
        try:
            return obj.proposal.approval.lodgement_number
        except:
            return ''

    def get_applicant(self,obj):
        try:
            return obj.proposal.approval.applicant
        except:
            return ''

    def get_org_applicant(self,obj):
        try:
            return obj.proposal.approval.org_applicant.name
        except:
            return ''

    def get_trading_name(self,obj):
        try:
            return obj.proposal.approval.org_applicant.organisation.trading_name
        except:
            return ''

    def get_proxy_applicant(self,obj):
        try:
            return obj.proposal.approval.proxy_applicant
        except:
            return ''

    def get_invoice_reference(self,obj):
        if obj and obj.invoices.last():
            return obj.invoices.last().invoice_reference
        return None

    def get_overdue(self,obj):
        if obj and obj.invoices.last():
            bi = obj.invoices.last()
            return bi.overdue
        return None

    def get_payment_status(self,obj):
        try:
            return obj.invoices.last().payment_status
        except:
            return 'Unpaid'

    def get_payment_method(self,obj):
        if obj and obj.invoices.last():
            inv = obj.invoices.last()
            return Invoice.objects.get(reference=inv.invoice_reference).get_payment_method_display()
        else:
            # if no invoice exists, likely this is booking is for monthly_invoicing
            return obj.get_booking_type_display()
 

class OverdueBookingInvoiceSerializer(serializers.ModelSerializer):
    invoice_reference = serializers.SerializerMethodField(read_only=True)
    overdue = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = BookingInvoice
        fields = (
            'id',
            'invoice_reference',
            'overdue',
        )

    def get_invoice_reference(self,obj):
        if obj and obj.booking.invoices.last():
            return obj.booking.invoices.last().invoice_reference
        return None

    def get_overdue(self,obj):
        if obj and obj.booking.invoices.last():
            bi = obj.booking.invoices.last()
            return bi.overdue
        return None


class DTBookingSerializer(serializers.ModelSerializer):
    #park_bookings = ParkBookingSerializer(many=True, read_only=True)
    application_fee_invoice = serializers.SerializerMethodField(read_only=True)
    approval_number = serializers.SerializerMethodField(read_only=True)
    applicant = serializers.SerializerMethodField(read_only=True)
    org_applicant = serializers.SerializerMethodField(read_only=True)
    trading_name = serializers.SerializerMethodField(read_only=True)
    proxy_applicant = serializers.SerializerMethodField(read_only=True)
    payment_status = serializers.SerializerMethodField(read_only=True)
    payment_method = serializers.SerializerMethodField(read_only=True)
    invoice_reference = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Booking
        fields = (
            'id',
            'admission_number',
            'application_fee_invoice',
            'approval_number',
            'applicant',
            'org_applicant',
            'trading_name',
            'proxy_applicant',
            'payment_status',
            'payment_method',
            'invoice_reference',  
        )
        datatables_always_serialize = (
            'id',
            'admission_number',
            'application_fee_invoice',
            'approval_number',
            'applicant',
            'org_applicant',
            'trading_name',
            'proxy_applicant',
            'payment_status',
            'payment_method',
            'invoice_reference',
        )

    def get_application_fee_invoice(self,obj):
        return obj.proposal.fee_invoice_reference

    def get_approval_number(self,obj):
        try:
            return obj.proposal.approval.lodgement_number
        except:
            return ''

    def get_applicant(self,obj):
        try:
            return obj.proposal.approval.applicant
        except:
            return ''

    def get_org_applicant(self,obj):
        try:
            return obj.proposal.approval.org_applicant.name
        except:
            return ''

    def get_trading_name(self,obj):
        try:
            return obj.proposal.approval.org_applicant.organisation.trading_name
        except:
            return ''

    def get_proxy_applicant(self,obj):
        try:
            return obj.proposal.approval.proxy_applicant
        except:
            return ''

    def get_invoice_reference(self,obj):
        if obj and obj.invoices.last():
            return obj.invoices.last().invoice_reference
        return None

    def get_overdue(self,obj):
        if obj and obj.invoices.last():
            bi = obj.invoices.last()
            return bi.overdue
        return None

    def get_payment_status(self,obj):
        try:
            return obj.invoices.last().payment_status
        except:
            return 'Unpaid'

    def get_payment_method(self,obj):
        if obj and obj.invoices.last():
            inv = obj.invoices.last()
            return Invoice.objects.get(reference=inv.invoice_reference).get_payment_method_display()
        else:
            # if no invoice exists, likely this is booking is for monthly_invoicing
            return obj.get_booking_type_display()

class DTParkBookingSerializer(serializers.ModelSerializer):
    park = serializers.SerializerMethodField(read_only=True)
    #booking=DTBookingSerializer(read_only=True)
    admission_number = serializers.SerializerMethodField(read_only=True)
    application_fee_invoice = serializers.SerializerMethodField(read_only=True)
    approval_number = serializers.SerializerMethodField(read_only=True)
    applicant = serializers.SerializerMethodField(read_only=True)
    org_applicant = serializers.SerializerMethodField(read_only=True)
    trading_name = serializers.SerializerMethodField(read_only=True)
    proxy_applicant = serializers.SerializerMethodField(read_only=True)
    payment_status = serializers.SerializerMethodField(read_only=True)
    payment_method = serializers.SerializerMethodField(read_only=True)
    invoice_reference = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ParkBooking
        fields = (
            'id',
            'park',
            'arrival',
            'no_adults',
            'no_children',
            'no_free_of_charge',
            'cost',
            'admission_number',
            'application_fee_invoice',
            'approval_number',
            'applicant',
            'org_applicant',
            'trading_name',
            'proxy_applicant',
            'payment_status',
            'payment_method',
            'invoice_reference',

        )
        datatables_always_serialize = (
            'id',
            'park',
            'arrival',
            'no_adults',
            'no_children',
            'no_free_of_charge',
            'cost',
            'admission_number',
            'application_fee_invoice',
            'approval_number',
            'applicant',
            'org_applicant',
            'trading_name',
            'proxy_applicant',
            'payment_status',
            'payment_method',
            'invoice_reference', 
        )

    def get_park(self,obj):
        return obj.park.name

    def get_admission_number(self,obj):
        return obj.booking.admission_number

    def get_application_fee_invoice(self,obj):
        return obj.booking.proposal.fee_invoice_reference

    def get_approval_number(self,obj):
        try:
            return obj.booking.proposal.approval.lodgement_number
        except:
            return ''

    def get_applicant(self,obj):
        try:
            return obj.booking.proposal.approval.applicant
        except:
            return ''

    def get_org_applicant(self,obj):
        try:
            return obj.booking.proposal.approval.org_applicant.name
        except:
            return ''

    def get_trading_name(self,obj):
        try:
            return obj.booking.proposal.approval.org_applicant.organisation.trading_name
        except:
            return ''

    def get_proxy_applicant(self,obj):
        try:
            return obj.booking.proposal.approval.proxy_applicant
        except:
            return ''

    def get_invoice_reference(self,obj):
        if obj.booking and obj.booking.invoices.last():
            return obj.booking.invoices.last().invoice_reference
        return None

    def get_overdue(self,obj):
        if obj.booking and obj.booking.invoices.last():
            bi = obj.booking.invoices.last()
            return bi.overdue
        return None

    def get_payment_status(self,obj):
        try:
            return obj.booking.invoices.last().payment_status
        except:
            return 'Unpaid'

    def get_payment_method(self,obj):
        if obj.booking and obj.booking.invoices.last():
            inv = obj.booking.invoices.last()
            return Invoice.objects.get(reference=inv.invoice_reference).get_payment_method_display()
        else:
            # if no invoice exists, likely this is booking is for monthly_invoicing
            return obj.booking.get_booking_type_display()
