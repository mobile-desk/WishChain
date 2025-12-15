from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from wishes.models.wish import Wish
from donations.models.donation import Donation
from partners.models import DonorProfile

@login_required
@require_POST
def grant_wish(request, wish_id):
    """Grant a wish - mark it as fulfilled and create a donation record"""
    try:
        wish = get_object_or_404(Wish, id=wish_id)
        
        # Check if wish is already fulfilled
        if wish.status == 'fulfilled':
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'message': 'This wish has already been fulfilled.'
                }, status=400)
            messages.warning(request, 'This wish has already been fulfilled.')
            return redirect('donations:donate')
        
        # Check if user already granted this wish
        if Donation.objects.filter(wish=wish, donor=request.user).exists():
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'message': 'You have already granted this wish.'
                }, status=400)
            messages.warning(request, 'You have already granted this wish.')
            return redirect('donations:donate')
        
        # Create donation record
        donation = Donation.objects.create(
            wish=wish,
            donor=request.user
        )
        
        # Update wish status
        wish.status = 'fulfilled'
        wish.save()
        
        # Update donor profile
        donor_profile, created = DonorProfile.objects.get_or_create(user=request.user)
        donor_profile.total_donations += 1
        donor_profile.update_impact_score()
        donor_profile.save()
        
        # Return JSON response for AJAX requests
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'message': f'You have successfully granted the wish: "{wish.title}"',
                'wish_id': wish.id
            })
        
        # Return redirect for regular form submissions
        messages.success(request, f'You have successfully granted the wish: "{wish.title}"')
        return redirect('donations:donate')
        
    except Exception as e:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'message': f'An error occurred: {str(e)}'
            }, status=500)
        
        messages.error(request, f'An error occurred while granting the wish: {str(e)}')
        return redirect('donations:donate')

