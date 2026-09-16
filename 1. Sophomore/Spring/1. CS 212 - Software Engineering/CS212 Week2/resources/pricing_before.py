# roomsvc/bookings.py — extract, lines 1103–1148, at tag cs212-reference
#
# Reproduced here so that A 2 Q2 can be attempted without cloning, and so that
# the "before" is fixed even if the reference tag moves. This is the open/closed
# case from L08 §2. Four switch sites exist on `kind`; this is one of them.
#
# The other three:
#   roomsvc/notify.py:88     — which template to render
#   roomsvc/reports.py:212   — which bookings count towards income
#   roomsvc/views.py:341     — which form fields to show
#
# Commit 7b1e4f2 (2024-03) added 'external_partner' and updated three of the four.

VAT = 0.20
RATE_PER_HOUR = 45.00


def price_for(booking):
    """Return the amount to invoice for a booking, in pounds."""
    hours = booking.duration_minutes / 60.0

    if booking.kind == 'lecture':
        price = 0.0
    elif booking.kind == 'seminar':
        price = 0.0
    elif booking.kind == 'external':
        price = RATE_PER_HOUR * hours * (1 + VAT)
    elif booking.kind == 'exam':
        price = 0.0
    elif booking.kind == 'external_charity':          # added 2023-09, 4b21c7d
        price = RATE_PER_HOUR * hours * 0.5 * (1 + VAT)
    elif booking.kind == 'external_partner':          # added 2024-03, 7b1e4f2
        price = RATE_PER_HOUR * hours * 0.8 * (1 + VAT)
    else:
        # Reached in production twice. Both times the kind was a typo written
        # by a direct database update; see incident notes for 2022-05-11.
        raise ValueError("unknown booking kind: %s" % booking.kind)

    # Equipment is never charged separately -- added 2022-01, no issue ref.
    if booking.resource.kind == 'EQUIPMENT':
        price = 0.0

    return round(price, 2)
