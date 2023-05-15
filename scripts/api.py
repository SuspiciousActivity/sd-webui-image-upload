import gradio as gr
import os
import paramiko
from fastapi import FastAPI

from modules import script_callbacks as script_callbacks
from modules.shared import opts

basedir = os.getcwd()

def get_option(opt: str, default):
	if hasattr(opts, opt):
		return opts[opt]
	return default

def uploadAPI(_: gr.Blocks, app: FastAPI):
	def sanitize_path(basepath: str, filename: str) -> str:
		filepath = os.path.join(basepath, filename)
		real_filepath = os.path.realpath(filepath)
		prefix = os.path.commonpath((basepath, real_filepath))

		if prefix == basepath:
			return real_filepath
		else:
			return None

	def upload(path):
		if not hasattr(opts, 'iu_server_host') or not hasattr(opts, 'iu_server_port') or not hasattr(opts, 'iu_server_user') or not hasattr(opts, 'iu_server_pass') or not hasattr(opts, 'iu_server_path'):
			print('Please configure all settings for Image Upload to use the extension.')
			return False

		try:
			print('Uploading ' + path)
			transport = paramiko.Transport((opts.iu_server_host, int(opts.iu_server_port)))
			transport.connect(username=opts.iu_server_user, password=opts.iu_server_pass)

			sftp = paramiko.SFTPClient.from_transport(transport)
			sftp.chdir(opts.iu_server_path)

			remote_filename = os.path.basename(path)
			sftp.put(path, remote_filename)

			sftp.close()
			transport.close()
			print('Upload complete')
			return True
		except Exception as e:
			raise e

	@app.post('/image-upload/{imgtype}/{name}')
	def upload_api(imgtype: str, name: str):
		folder={
			'txt2img': opts.outdir_txt2img_samples,
			'img2img': opts.outdir_img2img_samples,
			'extras': opts.outdir_extras_samples
		}
		folder = folder.get(imgtype, None)
		if folder == None:
			return False
		folder = os.path.realpath(os.path.join(basedir, folder))
		path = sanitize_path(folder, name)
		return upload(path)

script_callbacks.on_app_started(uploadAPI)
