
import Live # This allows us (and the Framework methods) to use the Live API on occasion
 # We will be using time functions for time-stamping our log file outputs

""" All of the Framework files are listed below, but we are only using using some of them in this script (the rest are commented out) """
from _Framework.ButtonElement import ButtonElement # Class representing a button a the controller

from _Framework.ButtonMatrixElement import ButtonMatrixElement # Class representing a 2-dimensional set of buttons
#from _Framework.ButtonSliderElement import ButtonSliderElement # Class representing a set of buttons used as a slider
 # Class attaching to the mixer of a given track
#from _Framework.ChannelTranslationSelector import ChannelTranslationSelector # Class switches modes by translating the given controls' message channel
 # Class representing a ClipSlot within Live
 # Base class for classes encompasing other components to form complex components
 # Base class for all classes representing control elements on a controller 
from _Framework.ControlSurface import ControlSurface # Central base class for scripts based on the new Framework
 # Base class for all classes encapsulating functions in Live
 # Class representing a device in Live
#from _Framework.DisplayDataSource import DisplayDataSource # Data object that is fed with a specific string and notifies its observers
from _Framework.EncoderElement import EncoderElement # Class representing a continuous control on the controller
from _Framework.InputControlElement import * # Base class for all classes representing control elements on a controller
#from _Framework.LogicalDisplaySegment import LogicalDisplaySegment # Class representing a specific segment of a display on the controller
from _Framework.MixerComponent import MixerComponent # Class encompassing several channel strips to form a mixer
 # Class for switching between modes, handle several functions with few controls
 # Class representing control elements that can send values
#from _Framework.PhysicalDisplayElement import PhysicalDisplayElement # Class representing a display on the controller
 # Class representing a scene in Live
from _Framework.SessionComponent import SessionComponent # Class encompassing several scene to cover a defined section of Live's session
from _Framework.SessionZoomingComponent import SessionZoomingComponent
from _Framework.SessionZoomingComponent import DeprecatedSessionZoomingComponent # Class using a matrix of buttons to choose blocks of clips in the session
 # Class representing a slider on the controller
from _Framework.TransportComponent import TransportComponent # Class encapsulating all functions in Live's transport section 17
from .SimpleButtonElement import SimpleButtonElement
from .ShiftableDeviceComponent import ShiftableDeviceComponent
from .FlashingButtonElement import FlashingButtonElement 
from .DC1_Map import * 
from .DC1_DEFS import *
from .DetailViewControllerComponent import DetailViewControllerComponent
from _Generic.Devices import *
from .CMDEncoderElement import CMDEncoderElement
from .ScrollEncoderElement import ScrollEncoderElement
from .LooperComponent import LooperComponent
# Global Variables
CHANNEL = 5 # assume channel is constant for everything
class DC1(ControlSurface):
    def __init__(self, c_instance):
        ControlSurface.__init__(self, c_instance)
        is_momentary = True
        self._timer = 0                             #used for flashing states, and is incremented by each call from self._update_display()
        self._touched = 0    
        self.flash_status = 1 # Used in FlashingButtonElement (kludge for our purposes)       
        self._device_selection_follows_track_selection = True
        
        with self.component_guard():
            self._setup_transport_control()

            if USE_MIXER_CONTROLS == True:
                self.mixer_control()
            if USE_SESSION_VIEW == True:
                self.session_control()        
            self.setup_device_control()
    
    
    def _setup_transport_control(self):
        is_momentary = True # We'll only be using momentary buttons here
        self.transport = TransportComponent() #Instantiate a Transport Component
        """set up the buttons"""
        self.transport.set_play_button(ButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL, 60)) #ButtonElement(is_momentary, msg_type, channel, identifier) Note that the MIDI_NOTE_TYPE constant is defined in the InputControlElement module
        self.transport.set_stop_button(ButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL, 61))
        self.transport.set_record_button(ButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL, 62))


    def mixer_control(self):
        is_momentary = True
        self.num_tracks = N_TRACKS
        if(USE_SENDS == True):
            self.mixer = MixerComponent(N_TRACKS, N_SENDS_PER_TRACK, USE_MIXER_EQ, USE_MIXER_FILTERS)
        else:
            self.mixer = MixerComponent(N_TRACKS,0, USE_MIXER_EQ, USE_MIXER_FILTERS)
        self.mixer.name = 'Mixer'
        self.mixer.set_track_offset(0) #Sets start point for mixer strip (offset from left)
        for index in range(N_TRACKS):
            self.mixer.channel_strip(index).name = 'Mixer_ChannelStrip_' + str(index)
            self.mixer.channel_strip(index)._invert_mute_feedback = True             


        if(USE_SELECT_BUTTONS == True):
            self.selectbuttons = [None for index in range(N_TRACKS)]
            for index in range(len(SELECT_BUTTONS)):
                self.selectbuttons[index] = FlashingButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL,SELECT_BUTTONS[index], 'Select_Button', self)
                self.mixer.channel_strip(index).set_select_button(self.selectbuttons[index])
                self.selectbuttons[index].set_on_value(SELECT_BUTTON_ON_COLOR)
                self.selectbuttons[index].set_off_value(SELECT_BUTTON_OFF_COLOR)

        if(USE_SOLO_BUTTONS == True):
            self.solobuttons = [None for index in range(N_TRACKS)]
            for index in range(len(SOLO_BUTTONS)):
                self.solobuttons[index] = FlashingButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL,SOLO_BUTTONS[index], 'Solo_Button', self)
                self.mixer.channel_strip(index).set_solo_button(self.solobuttons[index])
                self.solobuttons[index].set_on_value(SOLO_BUTTON_ON_COLOR)
                self.solobuttons[index].set_off_value(SOLO_BUTTON_OFF_COLOR)



        if(USE_ARM_BUTTONS == True):
            self.armbuttons = [None for index in range(N_TRACKS)]
            for index in range(len(ARM_BUTTONS)):
                self.armbuttons[index] = FlashingButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL,ARM_BUTTONS[index], 'Arm_Button', self)
                self.mixer.channel_strip(index).set_arm_button(self.armbuttons[index])
                self.armbuttons[index].set_on_value(ARM_BUTTON_ON_COLOR)
                self.armbuttons[index].set_off_value(ARM_BUTTON_OFF_COLOR)
		
        if(USE_MUTE_BUTTONS == True):
            self.mutebuttons = [None for index in range(N_TRACKS)]
            for index in range(len(MUTE_BUTTONS)):
                self.mutebuttons[index] = FlashingButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL,MUTE_BUTTONS[index], 'Mute_Button', self)
                self.mixer.channel_strip(index).set_mute_button(self.mutebuttons[index])
                self.mutebuttons[index].set_on_value(MUTE_BUTTON_ON_COLOR)
                self.mutebuttons[index].set_off_value(MUTE_BUTTON_OFF_COLOR)
                
        if(USE_SENDS == True):
            self.sendencoders = [None for index in range(len(SEND_ENCODERS))]
            for index in range(len(SEND_ENCODERS)):
                self.sendencoders[index] = EncoderElement(MIDI_CC_TYPE, CHANNEL, SEND_ENCODERS[index], Live.MidiMap.MapMode.absolute)
            for index in range(len(SEND_ENCODERS)/N_SENDS_PER_TRACK):
                self.mixer.channel_strip(index).set_send_controls(tuple(self.sendencoders[(index*N_SENDS_PER_TRACK):((index*N_SENDS_PER_TRACK)+N_SENDS_PER_TRACK-1)]))

                
        if(USE_VOLUME_CONTROLS == True):
            self.volencoders = [None for index in range(len(VOLUME_ENCODERS))]
            for index in range (len(VOLUME_ENCODERS)):
                self.volencoders[index] = EncoderElement(MIDI_CC_TYPE, CHANNEL, VOLUME_ENCODERS[index], Live.MidiMap.MapMode.absolute)
                self.mixer.channel_strip(index).set_volume_control(self.volencoders[index])
      
    def session_control(self):
        is_momentary = True
        self._timer = 0
        self.flash_status = 1
        self.grid = [None for index in range(N_TRACKS*N_SCENES)]
        for index in range(N_TRACKS*N_SCENES):
            self.grid[index] = FlashingButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL,TRACK_CLIP_BUTTONS[index], 'Grid' + str(index), self)
            self.grid[index].set_off_value(0)
            self.grid[index].turn_off()
            
        self.matrix = ButtonMatrixElement()
        for row in range(N_SCENES):
            button_row = []
            for column in range(N_TRACKS):
                button_row.append(self.grid[row+(column*N_SCENES)])
            self.matrix.add_row(tuple(button_row))
        self.session = SessionComponent(N_TRACKS,N_SCENES)
        self.session.name = "Session"
        self.session.set_offsets(0,0)

        self.scene = [None for index in range(N_SCENES)]
        for row in range(N_SCENES):
            self.scene[row] = self.session.scene(row)
            self.scene[row].name = 'Scene_'+str(row)
            for column in range(N_TRACKS):
                clip_slot = self.scene[row].clip_slot(column)
                clip_slot.name = str(column)+'_Clip_Slot'+str(row)
                self.scene[row].clip_slot(column).set_triggered_to_play_value(CLIP_TRG_PLAY_COLOR)
                self.scene[row].clip_slot(column).set_stopped_value(CLIP_STOP_COLOR)
                self.scene[row].clip_slot(column).set_started_value(CLIP_STARTED_COLOR)
        self.set_highlighting_session_component(self.session)        
        self.session_zoom = DeprecatedSessionZoomingComponent(self.session)                 #this creates the ZoomingComponent that allows navigation when the shift button is pressed
        self.session_zoom.name = 'Session_Overview'                            #name it so we can access it in m4l
        self.session_zoom.set_stopped_value(ZOOM_STOPPED)            #set the zooms stopped color
        self.session_zoom.set_playing_value(ZOOM_PLAYING)            #set the zooms playing color
        self.session_zoom.set_selected_value(ZOOM_SELECTED)            #set the zooms selected color
        self.session_zoom.set_button_matrix(self.matrix)                        #assign the ButtonMatrixElement that we created in _setup_controls() to the zooming component so that we can control it
        self._shift_button = ButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL, 63)
        self.session_zoom.set_zoom_button(self._shift_button)                   #assign a shift button so that we can switch states between the SessionComponent and the SessionZoomingComponent

        self.looper = LooperComponent(self)
        self.log_message(str(len(STOP_BUTTONS)))
        if(USE_STOP_BUTTONS == True):
            self.stopbuttons = [None for index in range(N_TRACKS)]
            for index in range(len(STOP_BUTTONS)):
                self.stopbuttons[index] = FlashingButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL,STOP_BUTTONS[index], 'Stop_Button', self)
                self.session.set_stop_track_clip_buttons(self.stopbuttons)
                self.stopbuttons[index].set_on_value(STOP_BUTTON_ON_COLOR)
                self.stopbuttons[index].set_off_value(STOP_BUTTON_OFF_COLOR)
        self.scrollencoder = ScrollEncoderElement(MIDI_CC_TYPE, CHANNEL, 32, Live.MidiMap.MapMode.absolute, self.session, self.transport, self.mixer, self.looper)
        self.scrollencoder.set_nav_button(ButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL, 0))
        self.scrollencoder.set_transport_button(ButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL, 7))
        self.scrollencoder.set_scene_button(ButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL, 3))
        self.scrollencoder.set_library_button(ButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL, 4))
        self.scrollencoder.set_button1(SimpleButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL, 1))
        self.scrollencoder.set_button2(SimpleButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL, 2))
        self.scrollencoder.set_button3(SimpleButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL, 5))
        self.scrollencoder.set_button4(SimpleButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL, 6))
        self.scrollencoder.set_encoder_button(SimpleButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL, 32))
		

        for column in range(N_TRACKS):
            for row in range(N_SCENES):
                self.scene[row].clip_slot(column).set_launch_button(self.grid[row+(column*N_SCENES)])    
    
        for index in range(N_TRACKS*N_SCENES):
            self.grid[index].clear_send_cache()      
                
        
        if USE_MIXER_CONTROLS == True:
            self.session.set_mixer(self.mixer)    

        self.refresh_state()
        self.session.set_enabled(True)
        self.session.update()  
              
    def setup_device_control(self):
        is_momentary = True
        device_bank_buttons = []
        device_param_controls = []
        bank_button_labels = ('Clip_Track_Button', 'Device_On_Off_Button', 'Previous_Device_Button', 'Next_Device_Button')
        for index in range(4):
            device_bank_buttons.append(ButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL, 16 + index))
            device_bank_buttons[-1].name = bank_button_labels[index]
        for index in range(8):
            #ring_mode_button = ButtonElement(not is_momentary, MIDI_CC_TYPE, CHANNEL, 21 + index)
            ringed_encoder = CMDEncoderElement(MIDI_CC_TYPE, CHANNEL, 16 + index, Live.MidiMap.MapMode.relative_binary_offset, 20)
            #ringed_encoder.set_ring_mode_button(ring_mode_button)
            ringed_encoder.name = 'Device_Control_' + str(index)
            #ring_mode_button.name = ringed_encoder.name + '_Ring_Mode_Button'
            device_param_controls.append(ringed_encoder)

        device = ShiftableDeviceComponent()
        device.name = 'Device_Component'
        device.set_bank_buttons(tuple(device_bank_buttons))
        device.set_shift_button(self._shift_button)
        device.set_parameter_controls(tuple(device_param_controls))
        device.set_on_off_button(device_bank_buttons[1])
        self.set_device_component(device)
        detail_view_toggler = DetailViewControllerComponent(self)
        detail_view_toggler.name = 'Detail_View_Control'
        detail_view_toggler.set_shift_button(self._shift_button)
        detail_view_toggler.set_device_clip_toggle_button(device_bank_buttons[0])
        detail_view_toggler.set_device_nav_buttons(device_bank_buttons[2], device_bank_buttons[3])
        
    def update_display(self):
        ControlSurface.update_display(self)
        self._timer = (self._timer + 1) % 256
  
    def disconnect(self):
        self._hosts = []
        ControlSurface.disconnect(self)
        return None        
