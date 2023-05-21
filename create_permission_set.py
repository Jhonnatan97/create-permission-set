import json
import time
import boto3

boto3.setup_default_session(profile_name='profile_name')

client = boto3.client(
    'sso-admin',
    region_name='sa-east-1',
   # aws_access_key_id='XXXXXXXXXXXXX',
   # aws_secret_access_key='XXXXXXXXXXXXXXXXXXXXXX',
   # aws_session_token='XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
)


pool_list = []
arn = 'arn:aws:sso:::instance/ssoins-XXXXXXXXXXXXXXXXXXX'
permission = 'arn:aws:sso:::permissionSet/ssoins-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
#CREATE PERMISSION SET
def create_permission_set():

    response = client.create_permission_set(
        Name='ViewOnlyAccess4',
        Description='teste',
        InstanceArn=arn,
        Tags=[
            {
                'Key': 'squad',
                'Value': 'ViewOnlyAccess4'
            },
        ]
    )['PermissionSet']
    print(response)

    #COLOCA A INLINE POLICY
    # response['PermissionSetArn']
    request = client.put_inline_policy_to_permission_set(
        InstanceArn=arn,
        PermissionSetArn=response['PermissionSetArn'],
        InlinePolicy=json.dumps(
            {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Effect": "Deny",
                        "Action": [
                            "secretsmanager:GetSecretValue",
                            "secretsmanager:DescribeSecret"
                        ],
                        "Resource": [
                            "arn:aws:secretsmanager:sa-east-1:XXXXXXXXXXXX:secret:*rds*"
                        ]
                    }
                ]
            }
        )
    )
    print('ATUALIZANDO A INLINE POLICY',request)

    #COLOCA A MANAGED POLICY (AWS)
    # response['PermissionSetArn']
    # request1 = client.attach_managed_policy_to_permission_set(
    #     InstanceArn=arn,
    #     PermissionSetArn=response['PermissionSetArn'],
    #     ManagedPolicyArn='arn:aws:iam::aws:policy/AmazonSageMakerFullAccess'
    # )
    # print(request1)

    #Bloco para atualizar as contas de uma permissionSet
    #     for account_id in pool_list:
    #         # print(account_id)
    #         time.sleep(3)
    #         account = client.provision_permission_set(
    #             InstanceArn=arn,
    #             PermissionSetArn=permission,
    #             TargetId=account_id,
    #             TargetType='AWS_ACCOUNT'
    #         )
    #         print(account)
    #     break
    #
    # print(pool_list)

#Lista todas as contas de uma permissionSet
def list_permission_set():
    response = client.list_accounts_for_provisioned_permission_set(
        InstanceArn=arn,
        PermissionSetArn=permission
    )

    for pool in response['AccountIds']:
        pool_list.append(pool)

    while 'NextToken' in response:

        response = client.list_accounts_for_provisioned_permission_set(InstanceArn=arn,
                                                                        PermissionSetArn=permission,
                                                                        NextToken=response["NextToken"])

        for pool in response['AccountIds']:
            pool_list.append(pool)
        print(pool_list)



    #Bloco para atualizar as contas de uma permissionSet
        for account_id in pool_list:
            # print(account_id)
            time.sleep(3)
            account = client.provision_permission_set(
                InstanceArn=arn,
                PermissionSetArn=permission,
                TargetId=account_id,
                TargetType='AWS_ACCOUNT'
            )
            print(account)
            print(account_id)
        break

    print(pool_list)

number = ['427229912516']
#provisionar contas em uma permissionSet
def account_provision_permissionset():
    for count in number:
        time.sleep(3)
        req = client.create_account_assignment(
            InstanceArn=arn,
            TargetId=count,
            TargetType='AWS_ACCOUNT',
            PermissionSetArn=permission,
            PrincipalType='USER',
            PrincipalId='XXXXXXXXXXXXXXXXXXXXXXXXX'
        )
        print(req)

#Deletar contas de uma PermissionSet
specific_account_assignments = {

    'Operations - Spec Serv Retail': {
        'groups': [
            {
                'group_name': 'Operations - Spec Serv Retail',
                'group_id': 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
            }
        ],
    }
}

def account_delete():
    response = client.list_accounts_for_provisioned_permission_set (
        InstanceArn=arn,
        PermissionSetArn=permission
    )

    for pool in response['AccountIds']:
        pool_list.append(pool)

    while 'NextToken' in response:
        response = client.list_accounts_for_provisioned_permission_set (InstanceArn=arn,
                                                                        PermissionSetArn=permission,
                                                                        NextToken=response["NextToken"])

        for pool in response['AccountIds']:
            pool_list.append(pool)
    print(pool_list)

    for count in pool_list:
        time.sleep(3)
        req = client.delete_account_assignment(
            InstanceArn=arn,
            TargetId=count,
            TargetType='AWS_ACCOUNT',
            PermissionSetArn=permission,
            PrincipalType='USER',
            PrincipalId='XXXXXXXXXXXXXXXXXXXXXXXXXXX'
        )
        print(req)
    print("Deletou todas as contas!!")

    #Deletar permissionSet
    response2 = client.delete_permission_set(
        InstanceArn=arn,
        PermissionSetArn=permission
    )
    print("PermissionSet deletada <3")

# create_permission_set()
# account_delete()
# account_provision_permissionset()
list_permission_set()