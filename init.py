import os
import eel.browsers as brw
import asyncio


_start_args = {
    'mode':             'chrome',                   # What browser is used
    'host':             'localhost',                # Hostname use for Bottle server
    'port':             8000,                       # Port used for Bottle server (use 0 for auto)
    'block':            True,                       # Whether start() blocks calling thread
    'jinja_templates':  None,                       # Folder for jinja2 templates
    'cmdline_args':     ['--disable-http-cache',' –disable-sync',' --disable-extensions'],   # Extra cmdline flags to pass to browser start
    'size':             None,                       # (width, height) of main window
    'position':         None,                       # (left, top) of main window
    'geometry':         {},                         # Dictionary of size/position for all windows
    'close_callback':   None,                       # Callback for when all windows have closed
    'app_mode':  True,                              # (Chrome specific option)
    'all_interfaces': False,                        # Allow bottle server to listen for connections on all interfaces
    'disable_cache': True,                          # Sets the no-store response header when serving assets
                       # Allows passing in a custom Bottle instance, e.g. with middleware
}

async def serverTask():
	os.system('python manage.py makemigrations')
	os.system('python manage.py migrate')
	os.system('python manage.py runserver')


async def clientTask():
	print("using client")
	brw.open(' ', _start_args)

async def main():
	server = asyncio.create_task(serverTask())
	client = asyncio.create_task(clientTask())

	client
	server
	


if __name__ == "__main__":
	asyncio.run(main())
