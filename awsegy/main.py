import click
import boto3
import os
import time
import progressbar


### Boto3 Configure
ec2_client = boto3.client('ec2', region_name = 'ap-northeast-2')

### Component Option 
def Search(Search):
    origin_idx = Search.replace(':',' ') 
    trans_idx = origin_idx.split()
    custom_filter = [{'Name':'tag:{}'.format(trans_idx[0]), 'Values': ['{}'.format(trans_idx[1])]}]
    response = ec2_client.describe_instances(Filters=custom_filter)
    return response['Reservations']

def ProgressBar(Number):
    bar = progressbar.ProgressBar(widgets=[' [', progressbar.Timer(), '] ', progressbar.Bar(), ' (', progressbar.ETA(), ') ',])
    for i in bar(range(Number)):
        time.sleep(0.1)

##############################
#### Main Commnad        #####
##############################
@click.group()
def cli():
    '''
    Interactive CLI tool awsegy \U0001f600
    '''
    pass


@click.command(help='Check your instance information!')
@click.argument('list')
def list(list):
    try:
        for instance in Search(list):
            print('\nInstance Id : '    + instance['Instances'][0]['InstanceId'])
            print('Publice Ip : '     + instance['Instances'][0]['PublicIpAddress'])
            print('Private Ip : '     + instance['Instances'][0]['PrivateIpAddress'])
            print('Instance State : ' + instance['Instances'][0]['State']['Name']+'\n')
    except:
        print('Oops! There''s no such name.')


@click.command(help='Please enter the instance type to change. (Stop Waiting Time=20sec')
@click.argument('change', nargs=2)
def change(change):
    for instance in Search(change[0]):
        ids = []
        id = instance['Instances'][0]['InstanceId']
        ids.append(id)
        if instance['Instances'][0]['State']['Name'] == 'running':
            print(f'Instance Stop Processing : {ids}')
            ec2_client.stop_instances(InstanceIds=ids)
            waiter=ec2_client.get_waiter('instance_stopped')
            ProgressBar(300)
            ec2_client.modify_instance_attribute(InstanceId=id, Attribute='instanceType', Value=change[1])
            ec2_client.start_instances(InstanceIds=ids)
            print(f'Instance Running : {ids}')
        else:
            ec2_client.modify_instance_attribute(InstanceId=id, Attribute='instanceType', Value=change[1])
            ec2_client.start_instances(InstanceIds=ids)
            print(f'Instance Running : {ids}')


@click.command(help='Tagging Instance')
@click.argument('tagging')
def tagging(tagging):
    print(tagging)
    





def main():
    cli.add_command(list)
    cli.add_command(change)
    cli.add_command(tagging)
    cli()

if __name__ == "__main__":
    main()








