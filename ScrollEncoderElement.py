from _Framework.ButtonElement import ButtonElement
from _Framework.CompoundComponent import CompoundComponent
from _Framework.EncoderElement import EncoderElement
from _Framework.SubjectSlot import subject_slot

class ScrollEncoderElement(EncoderElement,CompoundComponent):
	def __init__(self, msg_type, channel, identifier, map_mode, session, transport, mixer, looper):
		EncoderElement.__init__(self, msg_type, channel, identifier, map_mode)
		self.set_report_values(True, True)
		self.session = session
		self.transport = transport
		self.mixer = mixer
		self.looper = looper
		self.mode = 0
		self.nav_button = None
		self.scene_button = None
		self.library_button = None
		self.transport_button = None
		self.button1 = None
		self.button2 = None
		self.button3 = None
		self.button4 = None
		self.encoder_button = None
		self.null_button = ButtonElement(True, 0, channel,127)
	def update(self):
		pass
	def clear_in_buttons(self):
		if self.button4 != None:
			self.button1.turn_off()
			self.button2.turn_off()
			self.button3.turn_off()
			self.button4.turn_off()
	###button creation
	#top left button
	def set_nav_button(self, button):
		self.nav_button = button
		self.on_nav_value.subject = button
		self.update_out_buttons()
		button.send_value(1, True)
		self.set_nav_control()
	#top right button
	def set_scene_button(self, button):
		self.scene_button = button
		self.on_scene_value.subject = button
		self.update_out_buttons()
		button.send_value(0, True)
	#bottom left button
	def set_library_button(self, button):
		self.library_button = button
		self.on_library_value.subject = button
		self.update_out_buttons()
		button.send_value(0, True)
	#bottom right button
	def set_transport_button(self,button):
		self.transport_button = button
		self.on_transport_value.subject = button
		self.update_out_buttons()
		button.send_value(0, True)
	#top left encoder button
	def set_button1(self, button):
		self.button1 = button
		self.on_button1_value.subject = button
		self.update_in_buttons()
	#top right encoder button
	def set_button2(self, button):
		self.button2 = button
		self.on_button2_value.subject = button
		self.update_in_buttons()
	#bottom left encoder button
	def set_button3(self, button):
		self.button3 = button
		self.on_button3_value.subject = button
		self.update_in_buttons()
	#bottom right encoder button
	def set_button4(self, button):
		self.button4 = button
		self.on_button4_value.subject = button
		self.update_in_buttons()
		self.set_nav_control()
	#encoder button
	def set_encoder_button(self, button):
		self.encoder_button = button
		button.turn_on()
		button.send_value(127, True)
		self.on_encoder_button_value.subject = button
		self.update_in_buttons()
		
	####button actions
	@subject_slot('value')
	def on_nav_value(self, value):
		if value is not 0 or not self.nav_button.is_momentary():
			self.mode = 0
			self.clear_in_buttons()
			self.clear_transport_control()
			self.clear_scene_control()
			self.clear_library_control()
			self.set_nav_control()
			self.nav_button.send_value(1, True)
			self.scene_button.send_value(0, True)
			self.library_button.send_value(0, True)
			self.transport_button.send_value(0, True)
	@subject_slot('value')
	def on_scene_value(self, value):
		if value is not 0 or not self.scene_button.is_momentary():
			self.mode = 1
			
			self.clear_in_buttons()
			self.clear_nav_control()
			self.clear_transport_control()
			self.clear_library_control()
			self.set_scene_control()
			self.nav_button.send_value(0, True)
			self.scene_button.send_value(1, True)
			self.library_button.send_value(0, True)
			self.transport_button.send_value(0, True)
	@subject_slot('value')
	def on_library_value(self, value):
		if value is not 0 or not self.library_button.is_momentary():
			self.mode = 2
			
			self.clear_in_buttons()
			self.clear_nav_control()
			self.clear_transport_control()
			self.clear_scene_control()
			self.set_library_control()
			self.nav_button.send_value(0, True)
			self.scene_button.send_value(0, True)
			self.library_button.send_value(1, True)
			self.transport_button.send_value(0, True)
	@subject_slot('value')
	def on_transport_value(self, value):
		if value is not 0 or not self.transport_button.is_momentary():
			self.mode = 3
			
			self.clear_in_buttons()
			self.clear_nav_control()
			self.clear_scene_control()
			self.clear_library_control()
			self.set_transport_control()
			self.nav_button.send_value(0, True)
			self.scene_button.send_value(0, True)
			self.library_button.send_value(0, True)
			self.transport_button.send_value(1, True)
	
	
	def set_nav_control(self):
		#set left right
		self.session.set_track_bank_buttons(self.button2, self.button1)
		#set tempo
		self.transport.set_tap_tempo_button(self.button3)
		#set stop all
		self.session.set_stop_all_clips_button(self.button4)
	def clear_nav_control(self):
	
		self.session.set_track_bank_buttons(self.null_button, self.null_button)
		self.transport.set_tap_tempo_button(self.null_button)
		self.session.set_stop_all_clips_button(self.null_button)
	def set_scene_control(self):
		#self.session.set_select_buttons(self.button4, self.button1)
		self.mixer.set_select_buttons(self.button2, self.button1)
		self.transport.set_tap_tempo_button(self.button3)
		self.session.selected_scene().set_launch_button(self.button4)
		pass
	def clear_scene_control(self):
		#self.session.set_select_buttons(self.null_button, self.null_button)
		self.mixer.set_select_buttons(self.null_button, self.null_button)
		self.transport.set_tap_tempo_button(self.null_button)
		self.session.selected_scene().set_launch_button(self.null_button)
		#self.session.set_select_next_button(self.null_button)
		pass
	def set_library_control(self):
		self.looper.set_loop_double_button(self.button2)
		self.looper.set_loop_halve_button(self.button1)
		self.looper.set_loop_start_button(self.button3)
		self.looper.set_shift_button(self.button4)
		self.looper.set_loop_toggle_button(self.encoder_button)
		pass
	def clear_library_control(self):
		self.looper.set_loop_double_button(self.null_button)
		self.looper.set_loop_halve_button(self.null_button)
		self.looper.set_loop_start_button(self.null_button)
		self.looper.set_shift_button(self.null_button)
		self.looper.set_loop_toggle_button(self.null_button)
	def set_transport_control(self):
		self.transport.set_play_button(self.button1)
		self.transport.set_stop_button(self.button2)
		self.transport.set_record_button(self.button3)
		self.transport.set_overdub_button(self.button4)
	def clear_transport_control(self):
		self.transport.set_play_button(self.null_button)
		self.transport.set_stop_button(self.null_button)
		self.transport.set_record_button(self.null_button)
		self.transport.set_overdub_button(self.null_button)
	
	
	@subject_slot('value')
	def on_button1_value(self, value):
		if value is not 0 or not self.button1.is_momentary():
			if self.mode == 0: #nav mode
				pass
			elif self.mode == 1: #scene mode
				pass
			elif self.mode == 2: #library mode
				pass
			elif self.mode == 3: #transport mode
				pass
	@subject_slot('value')
	def on_button2_value(self, value):
		if value is not 0 or not self.button2.is_momentary():
			if self.mode == 0: #nav mode
				pass
			elif self.mode == 1: #scene mode
				pass
			elif self.mode == 2: #library mode
				pass
			elif self.mode == 3: #transport mode
				pass
	@subject_slot('value')
	def on_button3_value(self, value):
		if value is not 0 or not self.button3.is_momentary():
			if self.mode == 0: #nav mode
				pass
			elif self.mode == 1: #scene mode
				pass
			elif self.mode == 2: #library mode
				pass
			elif self.mode == 3: #transport mode
				pass
	@subject_slot('value')
	def on_button4_value(self, value):
		if value is not 0 or not self.button4.is_momentary():
			if self.mode == 0: #nav mode
				pass
			elif self.mode == 1: #scene mode
				pass
			elif self.mode == 2: #library mode
				pass
			elif self.mode == 3: #transport mode
				pass
	@subject_slot('value')
	def on_encoder_button_value(self, value):
		if value is not 0 or not self.encoder_button.is_momentary():
			if self.mode == 0: #nav mode
				pass
			elif self.mode == 1: #scene mode
				self.looper.get_current_clip()
				if self.looper._current_clip != None:
					self.looper._current_clip.fire()
			elif self.mode == 2: #library mode
				pass
			elif self.mode == 3: #transport mode
				pass
	def update_out_buttons(self):
		pass
	def update_in_buttons(self):
		pass
	def notify_value(self, value):
		super(EncoderElement, self).notify_value(value)
		if self.mode == 0: #nav mode
			if value>63 and self.session._can_bank_down() == True:
					self.session._change_offsets(0, 1)
			elif self.session._can_bank_up() == True:
					self.session._change_offsets(0, -1)
		elif self.mode == 1: #scene mode
			if value>63 and self.session._can_bank_down() == True:
				selected_scene = self.session.song().view.selected_scene
				all_scenes = self.session.song().scenes
				if selected_scene != all_scenes[-1]:
					index = list(all_scenes).index(selected_scene)
					self.session.song().view.selected_scene = all_scenes[index + 1]
			else:
				selected_scene = self.session.song().view.selected_scene
				all_scenes = self.session.song().scenes
				if selected_scene != all_scenes[0]:
					index = list(all_scenes).index(selected_scene)
					self.session.song().view.selected_scene = all_scenes[index - 1]
		elif self.mode == 2: #library mode
			if value>63:
				self.looper.move_start_marker(1)
			else:
				self.looper.move_start_marker(-1)
		elif self.mode == 3: #transport mode
			if value>63:
					#self.transport._ffwd_task = self.transport._tasks.add(partial(self.transport._move_current_song_time, 10.0))
					self.transport.song().current_song_time += 1
			else:
					#self.transport._rwd_task = self.transport._tasks.add(partial(self.transport._move_current_song_time, -10.0))
					if self.transport.song().current_song_time > 0:
						self.transport.song().current_song_time -= 1
		if self.normalized_value_listener_count():
			normalized = self.relative_value_to_delta(value) / 64.0 * self.encoder_sensitivity
			self.notify_normalized_value(normalized)
			