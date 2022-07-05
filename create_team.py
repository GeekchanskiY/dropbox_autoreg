html = s.get("https://www.dropbox.com/business/try?sku=std").text
        now = datetime.now()
        request_id = html.split("request_id=")[1].split(";")[0].replace("&amp", "")
        user_id = html.split('{"users": [{"userId": ')[1].split(",")[0]
        print(user_id)
        #s.post("https://www.dropbox.com/teamswalogger", data={})
        with open("output.html", "w", encoding="utf-8") as f:
            f.write(html)
        time.sleep(5)
        end = datetime.now()
        t: str = s.cookies["t"]
        diff = (now - end).total_seconds() * 1000
        gg = s.post("https://www.dropbox.com/teamswalogger", data={
            "is_xhr": True,
            "t": t,
            "event_name": "react_checkout_try_action",
            "extra": {"type":"SubmitFormStart","flow":"PreSelect","sku":"standard","numberOfUsers":5,"schedule":"yearly","paymentmethod":"creditcard","country":"AF","roundtrip":"715.3"},
            "for_uids": f"[{user_id}]"
        })
        print(gg.text)
        print(f"This is request id: {request_id}")
        r = s.post("https://www.dropbox.com/business/ajax_create_team_try", data={
            "tos_agree": True,
            "t": t,
            "request_id": request_id,
            "is_xhr": True,
            "tracking_params": {},
            "signup_url": "https://www.dropbox.com/business/try?sku=std",
            "schedule_id": 2,
            'signup_tag': 'team',
            "signup_data": "",
            "birthdate_ts": "",
            "county_code": "BY",
            "country": "BY",
            "team_name": "wpoisdfert",
            "tos_version": 3,
            "team_num_users": 5,
            "billing_schedule": "yearly",
            "currency": "USD",
            "signup_type": "trial",
            "sub_change_plan": """{"scheduledSubState":{"addonSkus":{},"billingScheduleId":2,"licenseSkus":{"TEAMLIC-ST1Y":5},"planSku":"TEAM-ST3L5TVD1Y"},"subState":{"addonSkus":{},"billingScheduleId":2,"licenseSkus":{"TEAMLIC-STU":5},"planSku":"TEAM-ST3L5TVDU"},"expectedPriceToken":"v1;fields;{\"ba\":+0.00,+\"c\":+\"USD\",+\"ct\":+0.00,+\"da\":+0.00,+\"dp\":+0,+\"itvs\":+[{\"ie\":+\"2022-08-04+17:25:20.901446\",+\"is\":+\"2022-07-04+17:25:20.901446\"},+{\"ie\":+\"2022-08-04+17:25:20.901446\",+\"is\":+\"2022-07-04+17:25:20.901446\"}],+\"lit\":+[1,+7],+\"nli\":+2,+\"ot\":+0.00,+\"pa\":+0.00,+\"pi\":+150,+\"pp\":+0.00,+\"pv\":+[9,+9],+\"q\":+[1,+2],+\"si\":+100000,+\"st\":+0.00,+\"t\":+\"2022-07-04+17:25:21.563988\",+\"ta\":+0.00,+\"tcc\":+\"BY\",+\"tei\":+null,+\"tet\":+null,+\"ti\":+false,+\"tji\":+\"BY\",+\"tpi\":+\"BY\",+\"tt\":+0.00,+\"tz\":+null}@1656959121.0|{\"code\":+null,+\"dcode\":+null,+\"is_trial\":+true,+\"plan_id\":+null,+\"reseller_discount\":+null,+\"reseller_hash\":+null}"}""".replace("+", ""),
            "expected_price": """v1;fields;{"ba":+0.00,+"c":+"USD",+"ct":+0.00,+"da":+0.00,+"dp":+0,+"itvs":+[{"ie":+"2022-08-04+17:25:20.901446",+"is":+"2022-07-04+17:25:20.901446"},+{"ie":+"2022-08-04+17:25:20.901446",+"is":+"2022-07-04+17:25:20.901446"}],+"lit":+[1,+7],+"nli":+2,+"ot":+0.00,+"pa":+0.00,+"pi":+150,+"pp":+0.00,+"pv":+[9,+9],+"q":+[1,+2],+"si":+100000,+"st":+0.00,+"t":+"2022-07-04+17:25:21.563988",+"ta":+0.00,+"tcc":+"BY",+"tei":+null,+"tet":+null,+"ti":+false,+"tji":+"BY",+"tpi":+"BY",+"tt":+0.00,+"tz":+null}@1656959121.0|{"code":+null,+"dcode":+null,+"is_trial":+true,+"plan_id":+null,+"reseller_discount":+null,+"reseller_hash":+null}""".replace("+", ""),
            "product": "new_standard",
            "account_info_type": "existing",
            "send_conversion_data": True,
            "is_pre_select": True,
            "licenses": 5,
            "ignore_bad_emails_silently": True,
            "expected_price_amount": 0,
            "submit_seq": 0,
            "signup_referrer": "https://www.dropbox.com/plans?trigger=direct",
            "time_on_page_ms": diff
        })
        print("AAAAAAA")
        print(r.text)