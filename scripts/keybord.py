
#import necessary dependancies
from pynput import keyboard
import rospy
from geometry_msgs.msg import Twist

#create variables to update 
LINEAR_X = 0
ANGULAR_Z = 0

NOW = rospy.Time.now()

#when pressed, update the variables
def on_press(key):
    try:
        rospy.loginfo(key.char, "Pressed")
        global LINEAR_X
        global ANGULAR_Z

        #check for pressed key
        if key.char == "w":
            LINEAR_X = 1.0
        elif key.char == "a":
            ANGULAR_Z = -1.0
        elif key.char == "s":
            LINEAR_X = -1.0
        elif key.char == "d":
            ANGULAR_Z = 1.0
        else:
            pass

        #run for 60 seconds
        if rospy.Time.now() < NOW + rospy.Duration.from_sec(60):
            move_turtle()
        #shutdown after 60 seconds elapsed
        else:
            rospy.loginfo("Time limit reached")
            return False
        
    except AttributeError:
        rospy.loginfo('special key {0} pressed'.format(key))
    
#pass when key released
def on_release(key):
    if key == keyboard.Key.esc:
        # Stop listener
        rospy.loginfo("Pressed esc")
        return False

#main function
def move_turtle():

    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1) 
    
    mov = Twist()
    
    rate = rospy.Rate(10) #could be removed

    if not rospy.is_shutdown(): 
        mov.linear.x = LINEAR_X #update the linear velocity
        mov.linear.y = 0
        mov.linear.z = ANGULAR_Z #update angular velocity
        mov.angular.x= 0
        mov.angular.y=0
        mov.angular.z=0
        
        pub.publish(mov) #publish 
        rate.sleep(rate)

#start the code
if __name__ == "__main__":
    try:
        rospy.init_node('mover', anonymous=True)
        rospy.loginfo("Starting node")

        #pynput başka programda çalışıyor ama bunda çalışmıyor? Sanırım wsl ile ilgili(?)
        with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()

        rospy.loginfo("Shutting down")
    except rospy.ROSInterruptException:
        pass
