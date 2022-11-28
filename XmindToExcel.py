import sys
from xmindparser import xmind_to_dict, xmind_to_json
import os
import pandas as pd
from pprint import pprint


from PyQt5.QtWidgets import QMessageBox

from Tools import Tools
Tools = Tools()


class XmindToExcel():
    def __init__(self):
        super(XmindToExcel, self)
        #self.XMD_Path = XMD_Patch
        #self.EXCl_Path = EXCl_Path

    def search_model_id(self, model_name):
        return        

    def construct_case_dict(self, _function_index, _case_index, _file_name, _sheet_name, _model_name, _function_name,
                            _case_name, _pre_condition, _steps, _pre_result, _design, _case_priority, _require_num,
                            case_type, use_stage, case_status):
        case_dict = {}
        case_dict['用例编号'] = f'{_function_index}-{_case_index}'
        case_dict['文件名'] = _file_name
        case_dict['子系统'] = _sheet_name
        case_dict['模块'] = _model_name
        case_dict['所属模块'] = _function_name
        case_dict['相关研发需求'] = self.search_model_id(_model_name) if self.search_model_id(_model_name) else '/(#0)'
        case_dict['用例标题'] = _case_name
        case_dict['前置条件'] = _pre_condition
        case_dict['步骤'] = _steps
        case_dict['预期'] = _pre_result
        case_dict['关键词'] = _design
        case_dict['优先级'] = _case_priority if _case_priority else ''
        case_dict['需求编号'] = _require_num
        case_dict['用例类型'] = case_type
        case_dict['适用阶段'] = use_stage
        case_dict['用例状态'] = case_status

        return case_dict



    # 变量名申明
    function_index = None
    case_index = None
    file_name = None
    sheet_name = None
    model_name = None
    function_name = None
    case_name = None
    pre_condition = None
    steps = None
    pre_result = None
    design = None
    case_priority = None
    require_num = None
    case_type = None
    use_stage = None
    case_status = None



    def transfer_xmind_case(self, XMD_Path, SaveExclFilePath):
        #file_path = r'E:\工作code\pythonProject\MapDataToQgis\pyqt_study\Xmind_to_excel_frontEnd\导出工具包\test.xmind'
        file_path = XMD_Path
        data_collection: list = xmind_to_dict(os.path.normpath(file_path))
        case_list = []

        is_complete = True
        case_total_statisics = 0

        f = open("./process_log.log", 'w')
        for doc in data_collection:
            doc_name = doc['title']
            if doc.get('topics', None) is None:
                doc_data = [doc['topic']]
            else:
                doc_data = doc['topics']
            for file in doc_data:
                file_name = file['title']
                file_data = file['topics']
                for sheet in file_data:
                    sheet_name = sheet['title']
                    sheet_data = sheet['topics']
                    function_index = 0
                    for model in sheet_data:
                        model_name = model['title']
                        model_data = model['topics']
                        for function in model_data:
                            function_name = function['title']
                            function_index += 1
                            function_data = function['topics']
                            for case_i, case in enumerate(function_data, 1):
                                try:
                                    case_name = case['title']
                                    case_index = case_i
                                    case_data = case['topics']
                                    case_priority = case['makers'][0][-1:] if case.get('makers', None) else None
                                    for _pre_condition in case_data:
                                        pre_condition = _pre_condition['title']
                                        _pre_condition_data = _pre_condition['topics']
                                        for step in _pre_condition_data:
                                            steps = step['title']
                                            step_data = step['topics']
                                            for _pre_result in step_data:
                                                pre_result = _pre_result['title']
                                                pre_result_data = _pre_result['topics']
                                                for _design in pre_result_data:
                                                    design = _design['title']
                                                    design_data = _design['topics']
                                                    for _require in design_data:
                                                        require_num = _require['title']
                                                        require_data = _require.get('topics', None)
                                                    if require_data:
                                                        for _case_type in require_data:
                                                            case_type = _case_type['title']
                                                            case_type_data = _case_type.get('topics', None)
                                                            if case_type_data:
                                                                for _use_stage in case_type_data:
                                                                    use_stage = _use_stage['title']
                                                                    use_stage_data = _use_stage.get('topics', None)
                                                                    if use_stage_data:
                                                                        for _case_status in use_stage_data:
                                                                            case_status = _case_status['title']
                                                    case_total_statisics += 1
                                                    case_dict = self.construct_case_dict(function_index,
                                                                                    case_index,
                                                                                    file_name,
                                                                                    sheet_name,
                                                                                    model_name,
                                                                                    function_name,
                                                                                    case_name,
                                                                                    pre_condition,
                                                                                    steps, pre_result,
                                                                                    design,
                                                                                    case_priority,
                                                                                    require_num,
                                                                                    case_type,
                                                                                    use_stage,
                                                                                    case_status)
                                                    print(
                                                        '----------------------------------------------------------')
                                                    pprint(case_dict)
                                                    print(
                                                        '----------------------------------------------------------')
                                                case_list.append(case_dict)
                                except Exception as e:
                                    print(f"【{function_name}-{case_name}】解析失败")
                                    print(f"【{function_name}-{case_name}】解析失败", file=f)
                                    is_complete = False

        else:
            df = pd.DataFrame(case_list)
            savePath = Tools.get_OSInfo(SaveExclFilePath+"\\"+os.path.splitext(os.path.split(XMD_Path)[1])[0]+".xlsx")
            df.to_excel(savePath, index=False)
            # pprint(case_list)
            if is_complete == True:
                print(f'全部导出成功, 用例总数为: {case_total_statisics}', file=f)
            else:
                print(f"有部分用例失败, 请查看log日志: 当前导出用例数为：{case_total_statisics}", file=f)
        f.close()
        with open("./process_log.log", 'r') as _fs:
            error_content = _fs.readlines()


        return {
            "success": is_complete,
            "data": {
                "completed_cases_num": case_total_statisics,
                "case_path": os.path.splitext(XMD_Path)[0] + '.xlsx',
                "error_log": error_content,
                "error_log_name": "./process_log.log"
            }
        }











# if __name__ == "__main__":
#     __file = r'E:\工作code\pythonProject\MapDataToQgis\pyqt_study\Xmind_to_excel_frontEnd\导出工具包\test.xmind'
#     transfer_xmind_case(_file_path=__file)








