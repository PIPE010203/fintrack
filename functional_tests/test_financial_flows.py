from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from datetime import date


class RegistrationFlowTest(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.driver = webdriver.Chrome()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def test_user_registration_and_login(self):
        driver = self.driver
        wait = WebDriverWait(driver, 5)

        driver.get(self.live_server_url + '/usuarios/registro/')
        wait.until(EC.presence_of_element_located((By.TAG_NAME, 'form')))

        driver.find_element(By.NAME, 'username').send_keys('selenium_user')
        driver.find_element(By.NAME, 'password1').send_keys('TestPass123!')
        driver.find_element(By.NAME, 'password2').send_keys('TestPass123!')
        driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

        wait.until(EC.url_contains('/dashboard/'))
        self.assertIn('/dashboard/', driver.current_url)
        self.assertIn('selenium_user', driver.page_source)

        driver.find_element(By.LINK_TEXT, 'Cerrar sesión').click()
        wait.until(EC.url_contains('/usuarios/login/'))

        driver.find_element(By.NAME, 'username').send_keys('selenium_user')
        driver.find_element(By.NAME, 'password').send_keys('TestPass123!')
        driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

        wait.until(EC.url_contains('/dashboard/'))
        self.assertIn('/dashboard/', driver.current_url)


class GastoCRUDFlowTest(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.driver = webdriver.Chrome()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def setUp(self):
        from django.contrib.auth.models import User
        User.objects.create_user(username='crud_user', password='TestPass123!')

    def test_gasto_full_crud(self):
        driver = self.driver
        wait = WebDriverWait(driver, 5)

        driver.get(self.live_server_url + '/usuarios/login/')
        wait.until(EC.presence_of_element_located((By.NAME, 'username')))
        driver.find_element(By.NAME, 'username').send_keys('crud_user')
        driver.find_element(By.NAME, 'password').send_keys('TestPass123!')
        driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        wait.until(EC.url_contains('/dashboard/'))

        driver.get(self.live_server_url + '/transacciones/gastos/nuevo/')
        wait.until(EC.presence_of_element_located((By.TAG_NAME, 'form')))

        driver.find_element(By.NAME, 'descripcion').send_keys('Gasto funcional')
        driver.find_element(By.NAME, 'monto').send_keys('50000')
        Select(driver.find_element(By.NAME, 'categoria')).select_by_value('alimentacion')
        driver.find_element(By.NAME, 'fecha').send_keys(date.today().strftime('%Y-%m-%d'))
        driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

        wait.until(EC.url_contains('/transacciones/gastos/'))
        self.assertIn('Gasto funcional', driver.page_source)
        self.assertIn('50000', driver.page_source)


class IngresoCRUDFlowTest(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.driver = webdriver.Chrome()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def setUp(self):
        from django.contrib.auth.models import User
        User.objects.create_user(username='ingreso_user', password='TestPass123!')

    def test_ingreso_full_crud(self):
        driver = self.driver
        wait = WebDriverWait(driver, 5)

        driver.get(self.live_server_url + '/usuarios/login/')
        wait.until(EC.presence_of_element_located((By.NAME, 'username')))
        driver.find_element(By.NAME, 'username').send_keys('ingreso_user')
        driver.find_element(By.NAME, 'password').send_keys('TestPass123!')
        driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        wait.until(EC.url_contains('/dashboard/'))

        driver.get(self.live_server_url + '/transacciones/ingresos/nuevo/')
        wait.until(EC.presence_of_element_located((By.TAG_NAME, 'form')))

        driver.find_element(By.NAME, 'descripcion').send_keys('Ingreso funcional')
        driver.find_element(By.NAME, 'monto').send_keys('1500000')
        Select(driver.find_element(By.NAME, 'categoria')).select_by_value('salario')
        driver.find_element(By.NAME, 'fecha').send_keys(date.today().strftime('%Y-%m-%d'))
        driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

        wait.until(EC.url_contains('/transacciones/ingresos/'))
        self.assertIn('Ingreso funcional', driver.page_source)
        self.assertIn('1500000', driver.page_source)


class BudgetAlertFlowTest(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.driver = webdriver.Chrome()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def setUp(self):
        from django.contrib.auth.models import User
        from transacciones.models import Gasto
        self.user = User.objects.create_user(username='budget_user', password='TestPass123!')
        Gasto.objects.create(
            usuario=self.user, descripcion='Gasto alto', monto=120000,
            categoria='alimentacion', fecha=date.today()
        )

    def test_budget_alert_when_exceeded(self):
        driver = self.driver
        wait = WebDriverWait(driver, 5)

        driver.get(self.live_server_url + '/usuarios/login/')
        wait.until(EC.presence_of_element_located((By.NAME, 'username')))
        driver.find_element(By.NAME, 'username').send_keys('budget_user')
        driver.find_element(By.NAME, 'password').send_keys('TestPass123!')
        driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        wait.until(EC.url_contains('/dashboard/'))

        driver.get(self.live_server_url + '/presupuesto/nuevo/')
        wait.until(EC.presence_of_element_located((By.TAG_NAME, 'form')))
        Select(driver.find_element(By.NAME, 'categoria')).select_by_value('alimentacion')
        driver.find_element(By.NAME, 'limite').send_keys('100000')
        driver.find_element(By.NAME, 'mes').clear()
        driver.find_element(By.NAME, 'mes').send_keys(str(date.today().month))
        driver.find_element(By.NAME, 'anio').clear()
        driver.find_element(By.NAME, 'anio').send_keys(str(date.today().year))
        driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        wait.until(EC.url_contains('/presupuesto/'))

        self.assertIn('120', driver.page_source)
        self.assertIn('Ya alcanzaste', driver.page_source)

        driver.get(self.live_server_url + '/transacciones/gastos/')
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'page-body')))
        self.assertIn('Alimentaci', driver.page_source)


class ReportExportFlowTest(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.driver = webdriver.Chrome()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def setUp(self):
        from django.contrib.auth.models import User
        from transacciones.models import Gasto, Ingreso
        user = User.objects.create_user(username='report_user', password='TestPass123!')
        Gasto.objects.create(
            usuario=user, descripcion='Gasto reporte', monto=75000,
            categoria='transporte', fecha=date.today()
        )
        Ingreso.objects.create(
            usuario=user, descripcion='Ingreso reporte', monto=200000,
            categoria='salario', fecha=date.today()
        )

    def test_report_page_and_export_links_exist(self):
        driver = self.driver
        wait = WebDriverWait(driver, 5)

        driver.get(self.live_server_url + '/usuarios/login/')
        wait.until(EC.presence_of_element_located((By.NAME, 'username')))
        driver.find_element(By.NAME, 'username').send_keys('report_user')
        driver.find_element(By.NAME, 'password').send_keys('TestPass123!')
        driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        wait.until(EC.url_contains('/dashboard/'))

        driver.get(self.live_server_url + '/transacciones/reporte/')
        wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

        self.assertIn('Exportar PDF', driver.page_source)
        self.assertIn('Exportar Excel', driver.page_source)
