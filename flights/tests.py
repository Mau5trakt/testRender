from django.test import TestCase, Client
from .models import Flight, Airport, Passenger
from django.db.models import Max

class FlightTestCase(TestCase):

    def setUp(self):

        # crear aeropuertos
        a1 = Airport.objects.create(code="AAA", city="City A")
        a2 = Airport.objects.create(code="BBB", city="City B")

        # Crear los vuelos

        Flight.objects.create(origin=a1, destination=a2, duration=100)
        Flight.objects.create(origin=a1, destination=a1, duration=200)
        Flight.objects.create(origin=a1, destination=a2, duration=-200)
    
    def test_valid_flight(self):
        a1 = Airport.objects.get(code="AAA")
        a2 = Airport.objects.get(code="BBB")
        f = Flight.objects.get(origin=a1, destination=a2, duration=100)
        self.assertTrue(f.is_valid_flight)
    
    def test_depatures_count(self):
        # verificar que hayan 3 salidas desde el aeropuerto 1

        a = Airport.objects.get(code="AAA")
        self.assertEqual(a.departures.count(), 3)

    def test_arrivals_count(self):
        # verificar que solo se haya llegado 1 vez al aeropuerto AAA
        a = Airport.objects.get(code="AAA")
        self.assertEqual(a.arrivals.count(), 1)

    def test_invalid_flight_destination(self):
        # el origen y el destino es el mismo
        a1 = Airport.objects.get(code="AAA")
        f = Flight.objects.get(origin=a1, destination=a1)
        self.assertFalse(f.is_valid_flight())

    def test_invalid_flight_duration(self):
        # la duracion es negativa
        a1 = Airport.objects.get(code="AAA")
        a2 = Airport.objects.get(code="BBB")

        f = Flight.objects.get(origin=a1, destination=a2, duration=-200)

        self.assertFalse(f.is_valid_flight())

    def test_index(self):
        # Configurar el cliente para realizar solicitudes
        c = Client()

        # Enviar solicitud get a una ruta y almacenar la respuesta
        respose = c.get("/flights/")
        self.assertEqual(respose.status_code, 200)

        self.assertEqual(respose.context["flights"].count(), 3)

    def test_valid_flight_page(self):
        a1 = Airport.objects.get(code="AAA")
        f = Flight.objects.get(origin=a1, destination=a1)

        c = Client()
        response = c.get(f"/flights/{f.id}")

        self.assertEqual(response.status_code, 200)
    
    def test_invalid_flight_page(self):
        max_id = Flight.objects.all().aggregate(Max("id"))["id_max"]

        c = Client()
        response = c.get(f"/flights/{max_id + 1}")

        self.assertEqual(response.status_code, 404)

    def test_flight_page_passenger(self):
        f = Flight.objects.get(pk=1)

        p = Passenger.objects.create(first="Melanie", last="Arias")

        f.passengers.add(p)

        c = Client()

        response = c.get(f"flights/{f.id}")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["passengers"].count(), 1)
        