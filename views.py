"""ONE-2 authenticated landing; attendance features remain unimplemented.

Docs: docs/Requirements.md (F-01), docs/Spec.md (section 2).
"""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def home(request):
    """Show the signed-in user a safe dashboard shell (no attendance data)."""
    return render(request, "core/home.html")
