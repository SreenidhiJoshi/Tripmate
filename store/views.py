from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate, login ,logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm
from django import forms
from django.shortcuts import render, get_object_or_404
from store.models import Product  # Import your model

# def product_detail(request, pk):
#     product = product.objects.get(id=pk)
#     return render(request, 'product.html', {'product': product})  

# Create your views here.
# def product(request,pk):
#         products = Product.objects.get(id=pk)
#         return render(request, 'product.html', {'product': product})


from django.shortcuts import render
import folium
import osmnx as ox
import networkx as nx
from geopy.distance import geodesic
import json
import os

# Predefined locations
location_data = {
    "My Location": (17.4897, 78.3882),
    "Home": (17.4897, 78.3882),
    "Golconda Fort": (17.3823, 78.4016),
    "Charminar": (17.3616, 78.4747),
    "Salar Jung Museum": (17.3716, 78.4802),
    "Birla Mandir": (17.4062, 78.4691),
    "Chowmalla Palace": (17.3578, 78.4717),
    "Ramoji Film City": (17.366, 78.476),
}


import os
import folium
import networkx as nx
import osmnx as ox
from django.shortcuts import render
from django.conf import settings
from geopy.geocoders import Nominatim

# Predefined coordinates for known locations
KNOWN_LOCATIONS = {
    "Hyderabad": (17.3850, 78.4867),
    "Mumbai": (19.0760, 72.8777),
    "Bangalore": (12.9716, 77.5946),
    "Delhi": (28.7041, 77.1025),
}

def generate_map(request):
    geolocator = Nominatim(user_agent="geoapi")

    if request.method == "POST":
        selected_places = request.POST.getlist("places", [])  # Get list of places entered

        # Ensure the folder exists
        static_folder = os.path.join(settings.BASE_DIR, "mapapp/static/maps")
        os.makedirs(static_folder, exist_ok=True)

        # Default location if no input
        start_location = KNOWN_LOCATIONS.get(selected_places[0], (17.3850, 78.4867)) if selected_places else (17.3850, 78.4867)

        folium_map = folium.Map(location=start_location, zoom_start=12)

        # Get coordinates for each place
        waypoints = []
        for place in selected_places:
            if place in KNOWN_LOCATIONS:
                lat, lon = KNOWN_LOCATIONS[place]
            else:
                location = geolocator.geocode(place)
                if location:
                    lat, lon = location.latitude, location.longitude
                else:
                    continue  # Skip invalid locations

            waypoints.append((lat, lon))
            folium.Marker(location=(lat, lon), popup=place, icon=folium.Icon(color="red")).add_to(folium_map)

        # Generate Route using OSMnx
        if len(waypoints) > 1:
            graph = ox.graph_from_point(start_location, dist=20000, network_type="drive")
            route_nodes = []

            for lat, lon in waypoints:
                nearest_node = ox.distance.nearest_nodes(graph, X=lon, Y=lat)
                route_nodes.append(nearest_node)

            route_edges = []
            for i in range(len(route_nodes) - 1):
                try:
                    path = nx.shortest_path(graph, route_nodes[i], route_nodes[i + 1], weight="length")
                    route_edges.extend(path)
                except nx.NetworkXNoPath:
                    print(f"⚠️ No road connection between {selected_places[i]} and {selected_places[i + 1]}")

            route_coords = [(graph.nodes[node]["y"], graph.nodes[node]["x"]) for node in route_edges]
            if route_coords:
                folium.PolyLine(route_coords, color="blue", weight=3, opacity=0.7, tooltip="Route").add_to(folium_map)

        # Save map
        map_path = os.path.join(static_folder, "travel_route.html")
        folium_map.save(map_path)

        return render(request, "cart.html", {
            "map_path": "/static/maps/travel_route.html"
        })

    return render(request, "cart.html", {"map_path": None})







def product(request,pk):
    product = Product.objects.get(id=pk)
    return render(request, 'product.html', {'product':product })
   

def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products':products })


def about(request):
    return render(request, 'about.html', {}) 

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,("You Have Been Logged In!"))
            return redirect('home')
        else:
         messages.success(request,("There was an error pls try again..."))
         return redirect('home')
    else:
     return render(request, 'login.html', {}) 

def logout_user(request):
    logout(request)
    messages.success(request,("you have been logged out....Thanks..."))
    return redirect('home')

def register_user(request):
   form = SignUpForm()
   if request.method == "POST":
      form = SignUpForm(request.POST)
      if form.is_valid():
         form.save()
         username = form.cleaned_data['username']
         password = form.cleaned_data['password1']
         #log in user
         user = authenticate(username=username, password=password)
         login(request, user)
         messages.success(request,("you have registered sucessfully..."))
         return redirect('home')
      else:
         messages.success(request,("oops there was some mistake"))
         return redirect('register')
   else:
      return render(request,'register.html',{'form': form})
   
from django.shortcuts import render
import json

from django.shortcuts import render
import json

def travel_route(request):
    # Define places with coordinates
    famous_places = {
        "Charminar": [17.3616, 78.4747],
        "Golconda Fort": [17.3833, 78.4011],
        "Hussain Sagar": [17.4239, 78.4738],
        "Birla Mandir": [17.4062, 78.4691],
        "Salar Jung Museum": [17.3713, 78.4804]
    }

    # Convert dictionary keys (place names) to a list
    famous_places_list = list(famous_places.keys())

    # Get selected places from POST request
    selected_places = request.POST.getlist('places', [])  # Default to empty list

    # Send places & selected data to the template
    return render(request, 'cart.html', {
        'famous_places': famous_places_list,  # Ensure it's a list
        'places_with_coords': json.dumps(famous_places),  # Pass full data for JavaScript
        'selected_places': json.dumps(selected_places)
    })




def cart_view(request):
    cart_items = request.session.get('cart', [])  # Fetch cart items from session
    products = Product.objects.filter(id__in=cart_items)  # Retrieve product details
    return render(request, 'cart.html', {'cart_items': products})
