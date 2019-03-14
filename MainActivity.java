package com.smartheat.conor.smartheat;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.view.Window;
import android.view.WindowManager;
import android.widget.ImageView;
import android.widget.TextView;
import org.eclipse.paho.android.service.MqttAndroidClient;
import org.eclipse.paho.client.mqttv3.IMqttActionListener;
import org.eclipse.paho.client.mqttv3.IMqttMessageListener;
import org.eclipse.paho.client.mqttv3.IMqttToken;
import org.eclipse.paho.client.mqttv3.MqttClient;
import org.eclipse.paho.client.mqttv3.MqttException;
import org.eclipse.paho.client.mqttv3.MqttMessage;

public class MainActivity extends AppCompatActivity
{
    public static int HeatStatus;
    public static int LightStatus;
    public static int BlanketStatus;
    public static double TempValue;
    public static int MinTemp;
    public static int MaxTemp;
    public static int Loop = 1;

    ImageView HeatImageView;
    ImageView LightImageView;
    ImageView BlanketImageView;
    ImageView ThermoImageView;
    TextView TempText;
    TextView ThermoText;

    String MQTT = "tcp://18.203.92.71:1883";
    String clientId = MqttClient.generateClientId();
    public  MqttAndroidClient client = null;
    
    @Override
    protected void onCreate(Bundle savedInstanceState)
    {
        Log.d("TESTLOG", "Program Starting...");
        super.onCreate(savedInstanceState);
        this.getWindow().setFlags(WindowManager.LayoutParams.FLAG_FULLSCREEN, WindowManager.LayoutParams.FLAG_FULLSCREEN);
        this.requestWindowFeature(Window.FEATURE_NO_TITLE);
        this.setContentView(R.layout.activity_main);
        HeatImageView = findViewById(R.id.HeatImage);
        LightImageView = findViewById(R.id.LightImage);
        BlanketImageView = findViewById(R.id.BlanketImage);
        ThermoImageView  = findViewById(R.id.ThermoImage);

        client = new MqttAndroidClient(getApplicationContext(), MQTT,clientId);

        HeatImageView.setOnClickListener(new View.OnClickListener()
        {
            @Override
            public void onClick(View v)
            {
                Log.d("TESTLOG", "Heat Clicked");

                try
                {
                    client.connect().setActionCallback(new IMqttActionListener()
                    {
                        @Override
                        public void onSuccess(IMqttToken asyncActionToken)
                        {

                            Log.d("MQTT", "Connected to Mosquito");

                            String ID = "1";
                            MqttMessage message = new MqttMessage(ID.getBytes());
                            try
                            {
                                client.publish("Toggle",message);
                            }
                            catch (MqttException e)
                            {
                                e.printStackTrace();
                            }
                        }
                        @Override
                        public void onFailure(IMqttToken asyncActionToken, Throwable exception)
                        {
                            Log.d("MQTT", "Failed to Connect to Mosquito");
                        }
                    });
                }
                catch (MqttException e)
                {
                    e.printStackTrace();
                }
            }
        });
        LightImageView.setOnClickListener(new View.OnClickListener()
        {
            @Override
            public void onClick(View v)
            {
                Log.d("MQTT", "Light Clicked");

                try
                {
                    client.connect().setActionCallback(new IMqttActionListener()
                    {
                        @Override
                        public void onSuccess(IMqttToken asyncActionToken)
                        {

                            Log.d("MQTT", "Connected to Mosquito");

                            String ID = "2";
                            MqttMessage message = new MqttMessage(ID.getBytes());
                            try
                            {
                                client.publish("Toggle",message);
                            }
                            catch (MqttException e)
                            {
                                e.printStackTrace();
                            }
                        }
                        @Override
                        public void onFailure(IMqttToken asyncActionToken, Throwable exception)
                        {
                            Log.d("MQTT", "Failed to Connect to Mosquito");
                        }
                    });
                }
                catch (MqttException e)
                {
                    e.printStackTrace();
                }
            }
        });
        BlanketImageView.setOnClickListener(new View.OnClickListener()
        {
            @Override
            public void onClick(View v)
            {
                Log.d("TESTLOG", "Blanket Clicked");
                try
                {
                    client.connect().setActionCallback(new IMqttActionListener()
                    {
                        @Override
                        public void onSuccess(IMqttToken asyncActionToken)
                        {

                            Log.d("MQTT", "Connected to Mosquito");

                            String ID = "3";
                            MqttMessage message = new MqttMessage(ID.getBytes());
                            try
                            {
                                client.publish("Toggle",message);
                            }
                            catch (MqttException e)
                            {
                                e.printStackTrace();
                            }
                        }
                        @Override
                        public void onFailure(IMqttToken asyncActionToken, Throwable exception)
                        {
                            Log.d("MQTT", "Failed to Connect to Mosquito");
                        }
                    });
                }
                catch (MqttException e)
                {
                    e.printStackTrace();
                }
            }
        });
        ThermoImageView.setOnClickListener(new View.OnClickListener()
        {
            @Override
            public void onClick(View v)
            {
                Log.d("TESTLOG", "Thermo Clicked");
                try
                {
                    client.connect().setActionCallback(new IMqttActionListener()
                    {
                        @Override
                        public void onSuccess(IMqttToken asyncActionToken)
                        {

                            Log.d("MQTT", "Connected to Mosquito");

                            String ID = "4";
                            MqttMessage message = new MqttMessage(ID.getBytes());
                            try
                            {
                                client.publish("Toggle",message);
                            }
                            catch (MqttException e)
                            {
                                e.printStackTrace();
                            }
                        }
                        @Override
                        public void onFailure(IMqttToken asyncActionToken, Throwable exception)
                        {
                            Log.d("MQTT", "Failed to Connect to Mosquito");
                        }
                    });
                }
                catch (MqttException e)
                {
                    e.printStackTrace();
                }
            }
        });
        Thread Sync = new Thread(new Runnable()
        {
            @Override
            public void run()
            {
                String clientId = MqttClient.generateClientId();
                final MqttAndroidClient client = new MqttAndroidClient(getApplicationContext(),MQTT,clientId);

                try
                {
                    client.connect().setActionCallback(new IMqttActionListener()
                    {
                        @Override
                        public void onSuccess(IMqttToken asyncActionToken)
                        {
                            Log.d("MQTT", "Connected to Mosquito");
                            String Topic = "DEVICES";

                            IMqttMessageListener iMqttMessageListener = new IMqttMessageListener()
                            {
                                @Override
                                public void messageArrived(String topic, MqttMessage message)
                                {

                                    String data = message.toString();
                                    String[] parts = data.split(",");
                                    Log.d("MQTT", "data:" + data);
                                    HeatStatus = Integer.parseInt(parts[0]);
                                    LightStatus = Integer.parseInt(parts[1]);
                                    BlanketStatus = Integer.parseInt(parts[2]);
                                    TempValue = Double.parseDouble(parts[3]);
                                    MinTemp = Integer.parseInt(parts[4]);
                                    MaxTemp = Integer.parseInt(parts[5]);
                                }
                            };
                            try
                            {
                                client.subscribe(Topic, 2, iMqttMessageListener);
                            }
                            catch (MqttException e)
                            {
                                e.printStackTrace();
                            }
                        }
                        @Override
                        public void onFailure(IMqttToken asyncActionToken, Throwable exception)
                        {
                            Log.d("MQTT", "Something went wrong e.g. connection timeout or firewall problems");
                        }
                    });
                }
                catch (MqttException e)
                {
                    e.printStackTrace();
                }
            }
        });

        Thread Graphics = new Thread(new Runnable()
        {
            int DisplayedHeatStatus = HeatStatus;
            int DisplayedLightStatus = LightStatus;
            int DisplayedBlanketStatus = BlanketStatus;
            double DisplayedTempValue = TempValue;
            int DisplayedMinTemp = MinTemp;

            @Override
            public void run()
            {
                while (Loop == 1)
                {
                    if (DisplayedHeatStatus != HeatStatus)
                    {
                        runOnUiThread(new Runnable()
                        {
                            @Override
                            public void run()
                            {
                                updateHeat();
                            }
                        });
                        DisplayedHeatStatus = HeatStatus;
                        Log.d("TESTLOG", "Updated Heater Graphic!");
                    }
                    if (DisplayedLightStatus != LightStatus)
                    {
                        runOnUiThread(new Runnable()
                        {
                            @Override
                            public void run()
                            {
                                updateLight();
                            }
                        });
                        DisplayedLightStatus = LightStatus;
                        Log.d("TESTLOG", "Updated Light Graphic!");
                    }
                    if (DisplayedBlanketStatus != BlanketStatus)
                    {
                        runOnUiThread(new Runnable()
                        {
                            @Override
                            public void run()
                            {
                                updateBlanket();
                            }
                        });
                        DisplayedBlanketStatus = BlanketStatus;
                        Log.d("TESTLOG", "Updated Blanket Graphic!");
                    }
                    if (DisplayedTempValue != TempValue)
                    {
                        runOnUiThread(new Runnable()
                        {
                            @Override
                            public void run()
                            {
                                updateTemp();
                            }
                        });
                        DisplayedTempValue = TempValue;
                        Log.d("TESTLOG", "Updated Temperature Value!");
                    }
                    if (DisplayedMinTemp != MinTemp)
                    {
                        runOnUiThread(new Runnable()
                        {
                            @Override
                            public void run()
                            {
                                updateThermoText();
                                updateThermo();
                            }
                        });
                        DisplayedMinTemp = MinTemp;
                        Log.d("TESTLOG", "Updated Thermo Value!");
                    }
                    try
                    {
                        Thread.sleep(100);
                    }
                    catch (InterruptedException e)
                    {
                        e.printStackTrace();
                    }
                }
            }
        });
        Sync.start();
        Graphics.start();
        boot();
    }
    public void boot()
    {
        updateHeat();
        updateLight();
        updateBlanket();
        updateThermo();
        updateTemp();
        updateThermoText();

        try
        {
            client.connect().setActionCallback(new IMqttActionListener()
            {
                @Override
                public void onSuccess(IMqttToken asyncActionToken)
                {

                    Log.d("MQTT", "Connected to Mosquito");

                    String ID = "0";
                    MqttMessage message = new MqttMessage(ID.getBytes());
                    try
                    {
                        client.publish("Toggle",message);
                    }
                    catch (MqttException e)
                    {
                        e.printStackTrace();
                    }
                }
                @Override
                public void onFailure(IMqttToken asyncActionToken, Throwable exception)
                {
                    Log.d("MQTT", "Failed to Connect to Mosquito");
                }
            });
        }
        catch (MqttException e)
        {
            e.printStackTrace();
        }
    }
    public void updateHeat()
    {
        if (HeatStatus == 0)
        {
            HeatImageView = findViewById(R.id.HeatImage);
            HeatImageView.setImageResource(R.drawable.heatoff);
        }
        else if (HeatStatus == 1)
        {
            HeatImageView = findViewById(R.id.HeatImage);
            HeatImageView.setImageResource(R.drawable.heaton);
        }
    }
    public void updateBlanket()
    {
        if (BlanketStatus == 0)
        {
            BlanketImageView = findViewById(R.id.BlanketImage);
            BlanketImageView.setImageResource(R.drawable.bedoff);
        }
        else if (BlanketStatus == 1)
        {
            BlanketImageView = findViewById(R.id.BlanketImage);
            BlanketImageView.setImageResource(R.drawable.bedon);
        }
    }
    public void updateLight()
    {
        if (LightStatus == 0)
        {
            LightImageView = findViewById(R.id.LightImage);
            LightImageView.setImageResource(R.drawable.lightoff);
        }
        else if (LightStatus == 1)
        {
            LightImageView = findViewById(R.id.LightImage);
            LightImageView.setImageResource(R.drawable.lighton);
        }
    }
    public void updateThermo()
    {
        if (MinTemp == 19)
        {
            ThermoImageView = findViewById(R.id.ThermoImage);
            ThermoImageView.setImageResource(R.drawable.thermo1);
        }
        else if (MinTemp == 20)
        {
            ThermoImageView = findViewById(R.id.ThermoImage);
            ThermoImageView.setImageResource(R.drawable.thermo2);
        }
        else if (MinTemp == 21)
        {
            ThermoImageView = findViewById(R.id.ThermoImage);
            ThermoImageView.setImageResource(R.drawable.thermo3);
        }
        else if (MinTemp == 22)
        {
            ThermoImageView = findViewById(R.id.ThermoImage);
            ThermoImageView.setImageResource(R.drawable.thermo4);
        }
    }
    public void updateTemp()
    {
        TempText = findViewById(R.id.TempText);
        String Message = "Temperature: " + TempValue + "°";
        TempText.setText(Message);
    }
    public void updateThermoText()
    {
        ThermoText = findViewById(R.id.ThermoText);
        String Message = "Min: "+ MinTemp + "° Max: " + MaxTemp + "°";
        ThermoText.setText(Message);
    }
}
