from ansible.module_utils.basic import AnsibleModule
import subprocess
import re

#Формат запуска модуля из консоли
#ansible all -m ping_hosts -a "hosts=ya.ru,mail.ru,localhost" 
#Предварительно установить ansible на локальной машине
#Закинуть модуль в папку с модулями

def run_module():
    #Аргументы модуля
    module_args = dict(
        hosts=dict(type='list', required=True)
    )
    #Формат ответа модуля
    result = dict(
        changed=False,
        response=''
    )
    #Инстанцируем модуль
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )
    #Создаем регулярное выражение
    regex = re.compile('(\\n)')
    answer =''
    #Пробегаемся по нужным хостам
    for x in module.params['hosts']:
        #Формируем подпроцесс на удаленном узле
        result_ping = subprocess.Popen(["ping", x, "-c", "1"],stdout=subprocess.PIPE)
        #Ждем его окончания
        result_ping.wait()
        #Читаем результат выполнения процесса
        temp_result = result_ping.stdout.read()
        #Достаем последнюю строчку с помощью регулярки и прибавляем ее к предыдущим
        answer = answer + x +':' + regex.split(temp_result)[-3] + ';'
    #Устанавливаем ответ молуля
    result['response'] = answer
    #Завершаем работу модуля
    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()
