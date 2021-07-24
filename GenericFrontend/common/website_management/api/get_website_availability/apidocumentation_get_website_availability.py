# API Logic
"""
This api returns the website's launch_flag and state_flag by
calling the sql function sp_fetch_website_maintainance_flags.
Below is the action that the front end will take based on the output.

live_flag	state_flag	What to show
0	        0	        show "we are coming soon" page
0	        1	        show "we are coming soon" page
1	        0       	show "Under maintainance" page
1	        1	        show home page or navigate to user's page of choice. In other words website should behave as it should.

"""

# API Input
"""
NO additional input required apart from APIDetails
"""

# API Output
"""
    {
        'live_flag': 1,
        'state_flag': 1
    }
"""
